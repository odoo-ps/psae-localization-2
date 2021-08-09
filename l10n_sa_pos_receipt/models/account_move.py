import base64

from odoo import fields, api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    narration = fields.Text(translate=True)
    amount_total_words_primary = fields.Char(compute="_compute_amount_to_words")
    amount_total_words_secondary = fields.Char(compute="_compute_amount_to_words")
    delivery_date = fields.Date(string="Delivery Date", required=True)
    invoice_date = fields.Date(required=True)
    qr_code_str = fields.Char(compute="_compute_qr_code_str")
    confirmation_datetime = fields.Datetime(default=False, readonly=True)

    @api.depends("amount_total", "amount_untaxed", "confirmation_datetime", "company_id", "company_id.vat")
    def _compute_qr_code_str(self):
        for record in self:
            record.qr_code_str = ""
            if record.confirmation_datetime:
                company_name_byte_array = record.company_id.display_name.encode('UTF-8')
                company_name_tag_encoding = (1).to_bytes(length=1, byteorder='big')
                company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
                company_name_enc = company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

                company_vat_byte_array = record.company_id.vat.encode('UTF-8')
                company_vat_tag_encoding = (2).to_bytes(length=1, byteorder='big')
                company_vat_length_encoding = len(company_vat_byte_array).to_bytes(length=1, byteorder='big')
                company_vat_enc = company_vat_tag_encoding + company_vat_length_encoding + company_vat_byte_array

                timestamp_byte_array = record.confirmation_datetime.isoformat().encode('UTF-8')
                timestamp_tag_encoding = (3).to_bytes(length=1, byteorder='big')
                timestamp_length_encoding = len(timestamp_byte_array).to_bytes(length=1, byteorder='big')
                timestamp_enc = timestamp_tag_encoding + timestamp_length_encoding + timestamp_byte_array

                amount_total_byte_array = str(record.amount_total).encode('UTF-8')
                amount_total_tag_encoding = (4).to_bytes(length=1, byteorder='big')
                amount_total_length_encoding = len(amount_total_byte_array).to_bytes(length=1, byteorder='big')
                amount_total_enc = amount_total_tag_encoding + amount_total_length_encoding + amount_total_byte_array

                total_vat_byte_array = str(record.currency_id.round(record.amount_total - record.amount_untaxed)).encode(
                    'UTF-8')
                total_vat_tag_encoding = (5).to_bytes(length=1, byteorder='big')
                total_vat_length_encoding = len(total_vat_byte_array).to_bytes(length=1, byteorder='big')
                total_vat_enc = total_vat_tag_encoding + total_vat_length_encoding + total_vat_byte_array

                record.qr_code_str = base64.b64encode(
                    company_name_enc + company_vat_enc + timestamp_enc + amount_total_enc + total_vat_enc).decode('UTF-8')

    @api.onchange("invoice_date", "delivery_date")
    def _onchange_invoice_or_delivery_date(self):
        if not self.delivery_date or self.delivery_date < self.invoice_date:
            self.update({"delivery_date": self.invoice_date})

    def action_post(self):
        for record in self:
            record.confirmation_datetime = fields.Datetime.now()
        super(AccountMove, self).action_post()


class POSOrder(models.Model):
    _inherit = "pos.order"

    qr_code_str = fields.Char(related="account_move.qr_code_str")

    @api.model
    def create_from_ui(self, orders, draft=False):
        """ Create and update Orders from the frontend PoS application.

        Create new orders and update orders that are in draft status. If an order already exists with a status
        diferent from 'draft'it will be discareded, otherwise it will be saved to the database. If saved with
        'draft' status the order can be overwritten later by this function.

        :param orders: dictionary with the orders to be created.
        :type orders: dict.
        :param draft: Indicate if the orders are ment to be finalised or temporarily saved.
        :type draft: bool.
        :Returns: list -- list of db-ids for the created and updated orders.
        """
        order_ids = []
        for order in orders:
            existing_order = False
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(
                    ['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])], limit=1)
            if (existing_order and existing_order.state == 'draft') or not existing_order:
                order_ids.append(self._process_order(order, draft, existing_order))

        return self.env['pos.order'].search_read(domain=[('id', 'in', order_ids)], fields=['id', 'pos_reference', 'qr_code_str'])
