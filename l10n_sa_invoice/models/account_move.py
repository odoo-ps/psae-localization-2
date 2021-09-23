# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    narration = fields.Text(translate=True)
    invoice_date = fields.Date(required=True, default=fields.Date.today)
    delivery_date = fields.Date(string="Delivery Date", required=True, default=fields.Date.today)
    qr_code_str = fields.Char(compute="_compute_qr_code_str")
    confirmation_datetime = fields.Datetime(default=False, readonly=True, copy=False)

    def _get_name_invoice_report(self):
        self.ensure_one()
        if self.company_id.secondary_language and self.company_id.invoice_text:
            return 'l10n_sa_invoice.ar_invoice'
        return super()._get_name_invoice_report()

    @api.depends("amount_total", "amount_untaxed", "confirmation_datetime", "company_id", "company_id.vat")
    def _compute_qr_code_str(self):
        for record in self:
            record.qr_code_str = ""
            if record.confirmation_datetime and record.company_id.vat:
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

                total_vat_byte_array = str(
                    record.currency_id.round(record.amount_total - record.amount_untaxed)).encode(
                    'UTF-8')
                total_vat_tag_encoding = (5).to_bytes(length=1, byteorder='big')
                total_vat_length_encoding = len(total_vat_byte_array).to_bytes(length=1, byteorder='big')
                total_vat_enc = total_vat_tag_encoding + total_vat_length_encoding + total_vat_byte_array

                record.qr_code_str = base64.b64encode(
                    company_name_enc + company_vat_enc + timestamp_enc + amount_total_enc + total_vat_enc).decode(
                    'UTF-8')

    @api.constrains("invoice_date", "delivery_date")
    def _delivery_date_constraint(self):
        for record in self:
            if record.delivery_date < record.invoice_date:
                raise UserError(
                    _(f"Delivery Date ({record.delivery_date}) cannot be before Invoice Date ({record.invoice_date})"))

    def action_post(self):
        for record in self:
            record.confirmation_datetime = fields.Datetime.now()
        super(AccountMove, self).action_post()
