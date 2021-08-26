# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import fields, api, models


class POSOrder(models.Model):
    _inherit = "pos.order"

    qr_code_str = fields.Char(compute="_compute_qr_code_str")

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
                    ['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])],
                    limit=1)
            if (existing_order and existing_order.state == 'draft') or not existing_order:
                order_ids.append(self._process_order(order, draft, existing_order))

        return self.env['pos.order'].search_read(domain=[('id', 'in', order_ids)],
                                                 fields=['id', 'pos_reference', 'qr_code_str'])

    @api.depends("amount_total", "amount_tax", "date_order", "company_id", "company_id.vat")
    def _compute_qr_code_str(self):
        for record in self:
            record.qr_code_str = ""
            if record.date_order and record.company_id.vat:
                company_name_byte_array = record.company_id.display_name.encode('UTF-8')
                company_name_tag_encoding = (1).to_bytes(length=1, byteorder='big')
                company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
                company_name_enc = company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

                company_vat_byte_array = record.company_id.vat.encode('UTF-8')
                company_vat_tag_encoding = (2).to_bytes(length=1, byteorder='big')
                company_vat_length_encoding = len(company_vat_byte_array).to_bytes(length=1, byteorder='big')
                company_vat_enc = company_vat_tag_encoding + company_vat_length_encoding + company_vat_byte_array

                timestamp_byte_array = record.date_order.isoformat().encode('UTF-8')
                timestamp_tag_encoding = (3).to_bytes(length=1, byteorder='big')
                timestamp_length_encoding = len(timestamp_byte_array).to_bytes(length=1, byteorder='big')
                timestamp_enc = timestamp_tag_encoding + timestamp_length_encoding + timestamp_byte_array

                amount_total_byte_array = str(record.amount_total).encode('UTF-8')
                amount_total_tag_encoding = (4).to_bytes(length=1, byteorder='big')
                amount_total_length_encoding = len(amount_total_byte_array).to_bytes(length=1, byteorder='big')
                amount_total_enc = amount_total_tag_encoding + amount_total_length_encoding + amount_total_byte_array

                total_vat_byte_array = str(record.amount_tax).encode('UTF-8')
                total_vat_tag_encoding = (5).to_bytes(length=1, byteorder='big')
                total_vat_length_encoding = len(total_vat_byte_array).to_bytes(length=1, byteorder='big')
                total_vat_enc = total_vat_tag_encoding + total_vat_length_encoding + total_vat_byte_array

                record.qr_code_str = base64.b64encode(
                    company_name_enc + company_vat_enc + timestamp_enc + amount_total_enc + total_vat_enc).decode(
                    'UTF-8')

    def _prepare_invoice_vals(self):
        self.ensure_one()
        vals = super(POSOrder, self)._prepare_invoice_vals()
        vals.update({"from_pos": True, "confirmation_datetime": self.date_order})
        return vals
