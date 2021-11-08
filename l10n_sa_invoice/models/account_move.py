# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_date = fields.Date(default=fields.Date.context_today, copy=False)
    show_delivery_date = fields.Boolean(compute='_get_show_delivery_date')
    qr_code_str = fields.Char(compute='_compute_qr_code_str')
    confirmation_datetime = fields.Datetime(default=False, readonly=True, copy=False)

    @api.depends('company_id.country_id')
    def _get_show_delivery_date(self):
        for move in self:
            move.show_delivery_date = move.company_id.country_id == self.env.ref('base.sa')

    @api.depends('amount_total', 'amount_untaxed', 'confirmation_datetime', 'company_id', 'company_id.vat')
    def _compute_qr_code_str(self):
        """ Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
        https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
        """
        def get_qr_encoding(tag, field):
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array

        for record in self:
            record.qr_code_str = ''
            if record.confirmation_datetime and record.company_id.vat:
                seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
                company_vat_enc = get_qr_encoding(2, record.company_id.vat)
                timestamp_enc = get_qr_encoding(3, record.confirmation_datetime.isoformat())
                invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
                total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(record.amount_total - record.amount_untaxed)))

                str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
                record.qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')

    def action_post(self):
        for record in self:
            if record.company_id.country_id == self.env.ref('base.sa') and record.delivery_date < record.invoice_date:
                raise UserError(_('Delivery Date cannot be before Invoice Date'))
        self.write({
            'confirmation_datetime': fields.Datetime.now()
        })
        return super().action_post()
