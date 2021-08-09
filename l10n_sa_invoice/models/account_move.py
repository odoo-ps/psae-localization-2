import base64
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class AccountMove(models.Model):
    _inherit = 'account.move'

    narration = fields.Text(translate=True)
    amount_total_words_primary = fields.Char(compute="_compute_amount_to_words")
    amount_total_words_secondary = fields.Char(compute="_compute_amount_to_words")
    delivery_date = fields.Date(string="Delivery Date", required=True)
    invoice_date = fields.Date(required=True)
    qr_code_str = fields.Char(compute="_compute_qr_code_str")
    confirmation_datetime = fields.Datetime(default=False, readonly=True)

    @api.depends('amount_residual')
    def _compute_amount_to_words(self):
        if num2words is not None:
            for record in self:
                if record.company_id.secondary_language and record.company_id.primary_language_code and record.company_id.secondary_language_code:
                    try:
                        record.amount_total_words_primary = num2words(record.amount_residual,
                                                                      lang=record.company_id.primary_language_code.code)
                    except NotImplementedError:
                        record.amount_total_words_primary = False
                    try:
                        record.amount_total_words_secondary = num2words(record.amount_residual,
                                                                        lang=record.company_id.secondary_language_code.code)
                    except NotImplementedError:
                        record.amount_total_words_secondary = False

    def _get_name_invoice_report(self):
        self.ensure_one()
        if self.company_id.secondary_language and self.company_id.invoice_text:
            return 'l10n_sa_invoice.ar_invoice'
        return super()._get_name_invoice_report()

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
