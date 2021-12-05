# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import base64
import json
from collections import defaultdict

from odoo import models, fields, api, _
import requests
from odoo.exceptions import ValidationError
from base64 import b64encode
import logging

from odoo.tools import formatLang

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_eg_invoice_sent = fields.Boolean('Document Sent', copy=False, tracking=True)
    l10n_eg_invoice_signed = fields.Boolean('Document Signed', copy=False, tracking=True)

    l10n_eg_long_id = fields.Char('ETA Long ID', copy=False)
    l10n_eg_internal_id = fields.Char('ETA Internal ID', copy=False)
    l10n_eg_hash_key = fields.Char('ETA Hash Key', copy=False)
    l10n_eg_uuid = fields.Char(string='Document UUID', copy=False)
    l10n_eg_submission_id = fields.Char(string='Submission ID', copy=False)
    l10n_eg_document_name = fields.Char('Document Name')
    l10n_eg_signature_type = fields.Char(string='Signature Type', copy=False)

    l10n_eg_pdf = fields.Binary(string='ETA PDF Document', copy=False)

    l10n_eg_state = fields.Selection([('submitted', 'Submitted'),
                                      ('valid', 'Valid'),
                                      ('invalid', 'Invalid'),
                                      ('rejected', 'Rejected'),
                                      ('cancelled', 'Cancelled')], string='ETA Status', copy=False, tracking=True)

    l10n_eg_signature_data = fields.Text('Signature Data', copy=False)

    l10n_eg_posted_date = fields.Datetime('Posted Date', copy=False)
    l10n_eg_amount_by_group = fields.Binary(string="Tax amount by group",
                                            compute='_compute_invoice_taxes_by_group_l10n_eg',
                                            help='Edit Tax amounts if you encounter rounding issues.')

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id')
    def _compute_invoice_taxes_by_group_l10n_eg(self):
        for move in self:

            # Not working on something else than invoices.
            if not move.is_invoice(include_receipts=True):
                move.l10n_eg_amount_by_group = []
                continue

            lang_env = move.with_context(lang=move.partner_id.lang).env
            balance_multiplicator = -1 if move.is_inbound() else 1

            tax_lines = move.line_ids.filtered('tax_line_id')
            base_lines = move.line_ids.filtered('tax_ids')

            tax_group_mapping = defaultdict(lambda: {
                'base_lines': set(),
                'base_amount': 0.0,
                'tax_amount': 0.0,
            })

            # Compute base amounts.
            for base_line in base_lines:
                base_amount = balance_multiplicator * (base_line.amount_currency if base_line.currency_id else base_line.balance)

                for tax in base_line.tax_ids.flatten_taxes_hierarchy():

                    if base_line.tax_line_id.tax_group_id == tax.tax_group_id:
                        continue

                    tax_group_vals = tax_group_mapping[tax.tax_group_id]
                    if base_line not in tax_group_vals['base_lines']:
                        tax_group_vals['base_amount'] += base_amount
                        tax_group_vals['base_lines'].add(base_line)

            # Compute tax amounts.
            for tax_line in tax_lines:
                tax_amount = balance_multiplicator * (tax_line.amount_currency if tax_line.currency_id else tax_line.balance)
                tax_group_vals = tax_group_mapping[tax_line.tax_line_id.tax_group_id]
                tax_group_vals['tax_amount'] += tax_amount

            tax_groups = sorted(tax_group_mapping.keys(), key=lambda x: x.sequence)
            l10n_eg_amount_by_group = []
            for tax_group in tax_groups:
                tax_group_vals = tax_group_mapping[tax_group]
                l10n_eg_amount_by_group.append((
                    tax_group.name,
                    tax_group_vals['tax_amount'],
                    tax_group_vals['base_amount'],
                    formatLang(lang_env, tax_group_vals['tax_amount'], currency_obj=move.currency_id),
                    formatLang(lang_env, tax_group_vals['base_amount'], currency_obj=move.currency_id),
                    len(tax_group_mapping),
                    tax_group.id
                ))
            move.l10n_eg_amount_by_group = l10n_eg_amount_by_group

    def action_post(self):
        res = super().action_post()
        self.filtered(lambda r: not r.l10n_eg_posted_date and r.state == 'posted').write({
            'l10n_eg_posted_date': fields.Datetime.now()
        })
        return res

    def _get_eta_api_domain(self):
        api_domain = self.env['ir.config_parameter'].sudo().get_param('default.eta.domain')
        if not api_domain:
            raise ValidationError(_('Please set API domain of ETA first.'))
        return api_domain

    def _get_eta_token_domain(self):
        token_domain = self.env['ir.config_parameter'].sudo().get_param('default.eta.token.domain')
        if not token_domain:
            raise ValidationError(_('Please set token domain of ETA first.'))
        return token_domain

    def _get_einvoice_token(self):
        token = False
        user = self.company_id.l10n_eg_client_identifier
        secret = self.company_id.l10n_eg_client_secret_1 or self.company_id.l10n_eg_client_secret_2
        access = '%s:%s' % (user, secret)
        user_and_pass = b64encode(bytes(access, encoding='utf8')).decode("ascii")
        token_domain = self._get_eta_token_domain()
        request_url = "%s/connect/token" % token_domain
        request_payload = {
            "grant_type": "client_credentials",
        }
        headers = {'Authorization': 'Basic ' + user_and_pass}
        try:
            request_response = requests.post(request_url, data=request_payload, headers=headers, timeout=(5, 10))
            if request_response:
                _logger.warning('%s.' % request_response.text)
                response_data = request_response.json()
                token = response_data.get('access_token')
            return token
        except Exception as ex:
            raise ValidationError(_('action code: 1006 \n%s' % ex))

    def action_send_eta_invoice(self):
        token = self._get_einvoice_token()
        uuid = self._action_send_eta_invoice(token)
        if uuid:
            self.l10n_eg_state = False
            self.l10n_eg_pdf = False
        return True

    def _action_send_eta_invoice(self, token):
        api_domain = self._get_eta_api_domain()
        request_url = "%s/api/v1/documentsubmissions" % api_domain
        eta_invoice = self._prepare_eta_invoice()
        request_payload = {
            "documents": [eta_invoice]
        }

        data = json.dumps(request_payload, ensure_ascii=False, indent=4).encode('utf-8')

        try:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
            request_response = requests.post(request_url, data=data, headers=headers, timeout=(5, 10))
            _logger.warning('Logger send response: %s.' % request_response)
            submission_data = request_response.json()
            if request_response:
                _logger.warning('Logger send response: %s.' % request_response.text)
            if submission_data:
                if submission_data.get('error'):
                    self._error_handeling(submission_data.get('error'), action_code='1002')

                if submission_data.get('rejectedDocuments', False) and isinstance(
                        submission_data.get('rejectedDocuments'), list):
                    self._error_handeling(submission_data.get('rejectedDocuments')[0].get('error'), action_code='1003')

                if submission_data.get('submissionId') and not submission_data.get('submissionId') is None:
                    if submission_data.get('acceptedDocuments'):
                        self.l10n_eg_invoice_sent = True
                        self.l10n_eg_submission_id = submission_data.get('submissionId')
                        uuid = submission_data.get('acceptedDocuments')[0].get('uuid')
                        self.l10n_eg_uuid = uuid
                        self.l10n_eg_long_id = submission_data.get('acceptedDocuments')[0].get('longId')
                        self.l10n_eg_internal_id = submission_data.get('acceptedDocuments')[0].get('internalId')
                        self.l10n_eg_hash_key = submission_data.get('acceptedDocuments')[0].get('hashKey')
                        return uuid

            return False
        except Exception as ex:
            raise ValidationError(_('action code: 1007 \n%s' % ex))

    def _get_eta_invoice(self, uuid, token=False):
        api_domain = self._get_eta_api_domain()
        request_url = "%s/api/v1/documents/%s/raw" % (api_domain, uuid)

        if not token:
            token = self._get_einvoice_token()
        request_payload = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        try:
            request_response = requests.request("GET", request_url, headers=headers, data=request_payload,
                                                timeout=(5, 10))
            if request_response:
                _logger.warning(
                    'GET Document: %s, response code: %s' % (request_response.text, request_response.status_code))
            if request_response.status_code in [404, 200]:
                return request_response.json()
            else:
                return {
                    "error": request_response.text
                }
        except Exception as ex:
            return {
                "error": _('Document cannot be reached. \n%s' % ex)
            }

    def _get_eta_invoice_pdf(self, uuid, token=False):
        api_domain = self._get_eta_api_domain()
        request_url = "%s/api/v1/documents/%s/pdf" % (api_domain, uuid)
        if not token:
            token = self._get_einvoice_token()
        request_payload = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        try:
            request_response = requests.request("GET", request_url, headers=headers, data=request_payload,
                                                timeout=(5, 10))
            _logger.warning('PDF Function Response %s.' % request_response)
            if request_response:
                _logger.warning('PDF Function %s.' % request_response.text)
            if request_response.status_code in [404, 200]:
                return request_response.content
            else:
                return {
                    "error": request_response.text
                }
        except Exception as ex:
            return {
                "error": _('PDF Not Reached. \n%s' % ex)
            }

    def _cancel_eta_invoice(self, uuid):
        api_domain = self._get_eta_api_domain()
        request_url = "%s/api/v1/documents/state/%s/state" % (api_domain, uuid)
        token = self._get_einvoice_token()
        request_payload = {
            "status": "cancelled",
            "reason": "Cancelled"
        }
        data = json.dumps(request_payload)
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        request_response = requests.request("PUT", request_url, headers=headers, data=data, timeout=(5, 10))
        if request_response:
            _logger.warning('%s.' % request_response.text)
        if request_response.status_code in [500, 400, 200]:
            get_invoice_data = request_response.json()
            return get_invoice_data
        else:
            return {
                "error": request_response.text
            }

    @api.model
    def get_default_sign_host(self):
        params = self.env['ir.config_parameter']
        sign_host = params.sudo().get_param('default.sign.host')
        if not sign_host:
            raise ValidationError(_('Please define the host of sign toll.'))
        return sign_host

    def action_post_sign_invoice(self):
        # TODO return a wizard with the json invoice
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'action_post_sign_invoice',
            'params': {
                'invoice_id': self.id,
            }
        }

    def action_cancel_eta_invoice(self):
        uuid = self.l10n_eg_uuid
        invoice = self._cancel_eta_invoice(uuid)
        if invoice is dict and invoice.get('error', False):
            self._error_handeling(invoice.get('error'), action_code='1004')
        else:
            self.l10n_eg_state = "cancelled"

    def action_get_eta_invoice_state(self, token=False, eta_uuid=False):
        uuid = eta_uuid
        if not eta_uuid:
            uuid = self.l10n_eg_uuid
        invoice = self._get_eta_invoice(uuid, token)
        if invoice.get('error', False):
            self._error_handeling(invoice.get('error'), action_code='1005')
        else:
            self.l10n_eg_state = invoice.get('status', False) and invoice['status'].lower()

        if invoice and 'validationResults' in invoice and isinstance(invoice['validationResults'], dict):
            self._set_validation(invoice['validationResults'])

    def action_update_eta_data(self):
        return {
            'name': _('Invoice (%s)' % self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('l10n_eg_invoice.view_invoice_update_uuid').id,
            'target': 'new',
            'res_id': self.id
        }

    def action_get_eta_invoice_pdf(self, token=False, uuid=False):
        if not uuid:
            uuid = self.l10n_eg_uuid
        invoice = self._get_eta_invoice_pdf(uuid, token)
        if isinstance(invoice, dict) and invoice.get('error', False):
            _logger.warning('PDF Content Error:  %s.' % invoice.get('error'))
        else:
            pdf = base64.b64encode(invoice)
            self.l10n_eg_pdf = pdf
            self.l10n_eg_document_name = "%s.pdf" % self.name.replace('/', '_')

    def _error_handeling(self, error_msg, action_code='1000'):
        _logger.warning('ERROR: %s.' % error_msg)
        if isinstance(error_msg, dict):
            message = ''
            property_path = ''
            ddetails = ''
            details = error_msg.get('details', False)
            if details and isinstance(details, list) and details[0]:
                message = details[0].get('message', '')
                property_path = details[0].get('propertyPath', '')
                ddetails = details[0].get('details', '')
            raise ValidationError(_('action code: %s\n%s. %s \n%s, %s, %s') % (action_code,
                                                                               error_msg.get('code', ''),
                                                                               error_msg.get('message', ''), message,
                                                                               property_path, ddetails))
        else:
            raise ValidationError(_('action code: %s\n %s' % (action_code, error_msg)))

    def _prepare_eta_invoice(self):
        total_discount = sum([(line.discount / 100.0) * line.quantity * line.price_unit for line in self.invoice_line_ids])
        total_sale_amount = sum([(line.quantity * line.price_unit) for line in self.invoice_line_ids])
        date_string = self.l10n_eg_posted_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        eta_invoice = {
            "issuer": self._prepare_issuer_data(),
            "receiver": self._prepare_receiver_data(),
            "documentType": "I" if self.move_type == 'out_invoice' else "c" if self.move_type == 'out_refund' else "d" if self.move_type == 'in_refund' else "",
            "documentTypeVersion": "1.0",
            "dateTimeIssued": date_string,
            "taxpayerActivityCode": self.company_id.partner_id.l10n_eg_activity_type,
            "internalID": self.name,
            "purchaseOrderReference": "",
            "purchaseOrderDescription": "",
            "salesOrderReference": self.invoice_origin or "",
            "salesOrderDescription": "",
            "proformaInvoiceNumber": "",
        }
        if self.move_type in ['out_refund', 'in_refund']:
            eta_invoice.update({
                'references': [
                    self.reversed_entry_id.l10n_eg_uuid] if self.move_type == 'out_refund' and self.reversed_entry_id and self.reversed_entry_id.l10n_eg_uuid else []
            })
        eta_invoice.update({
            "payment": self._prepare_payment_data(),
            "delivery": self._prepare_delivery_data(),
            "invoiceLines": self._prepare_invoice_lines_data(),
            "totalDiscountAmount": self._get_amount(total_discount) or 0,
            "totalSalesAmount": self._get_amount(total_sale_amount),
            "netAmount": self._get_amount(self.amount_untaxed),
            "taxTotals": [{
                "taxType": self.env['account.tax.group'].browse(tax[6]).l10n_eg_tax_code,
                "amount": self._get_amount(abs(tax[1])) or 0,
            } for tax in self.l10n_eg_amount_by_group],
            "totalAmount": self._get_amount(self.amount_total),
            "extraDiscountAmount": 0,
            "totalItemsDiscountAmount": 0,
            "signatures": [
                {
                    "signatureType": "I",
                    "value": self.l10n_eg_signature_data
                }
            ]
        })

        return eta_invoice

    def _prepare_issuer_data(self):
        company_partner = self.company_id.partner_id
        issuer = {
            "address": {
                "branchID": self.company_id.l10n_eg_branch_identifier,
                "country": company_partner.country_id.code,
                "governate": company_partner.state_id.name,
                "regionCity": company_partner.city,
                "street": company_partner.street,
                "buildingNumber": company_partner.l10n_eg_building_no,
                "postalCode": company_partner.zip or "",
                "floor": company_partner.l10n_eg_floor or "",
                "room": company_partner.l10n_eg_room or "",
                "landmark": company_partner.l10n_eg_landmark or "",
                "additionalInformation": company_partner.l10n_eg_additional_information or "",
            },
            "type": "B",
            "id": company_partner.l10n_eg_code,
            "name": self.company_id.name,
        }
        return issuer

    def _prepare_receiver_data(self):
        partner = self.partner_id
        receiver = {
            "address": {
                "country": partner.country_id.code,
                "governate": partner.state_id.name,
                "regionCity": partner.city,
                "street": partner.street,
                "buildingNumber": partner.l10n_eg_building_no,
                "postalCode": partner.zip or "",
                "floor": partner.l10n_eg_floor or "",
                "room": partner.l10n_eg_room or "",
                "landmark": partner.l10n_eg_landmark or "",
                "additionalInformation": partner.l10n_eg_additional_information or "",
            },
            "type": "B" if partner.company_type == 'company' and partner.country_id.code == 'EG' else "P" if partner.company_type == 'person' and partner.country_id.code == 'EG' else "F",
            "id": partner.l10n_eg_code or partner.vat if partner.company_type == 'company' else partner.l10n_eg_national_identifier or partner.vat,
            "name": partner.name,
        }
        return receiver

    def _prepare_payment_data(self):
        if not self.partner_bank_id:
            return {
                "bankName": "",
                "bankAddress": "",
                "bankAccountNo": "",
                "bankAccountIBAN": "",
                "swiftCode": "",
                "terms": ""
            }
        bank = self.partner_bank_id
        payment = {
            "bankName": bank.bank_id.name,
            "bankAddress": "%s" % bank.bank_id.street,
            "bankAccountNo": bank.acc_number,
            "bankAccountIBAN": "",
            "swiftCode": "",
            "terms": "",
        }
        return payment

    # FIXME need to filled
    def _prepare_delivery_data(self):
        delivery = {
            "approach": "",
            "packaging": "",
            "dateValidity": "",
            "exportPort": "",
            "grossWeight": 0,
            "netWeight": 0,
            "terms": ""
        }
        return delivery

    def _prepare_invoice_lines_data(self):
        lines = []
        for line in self.invoice_line_ids:
            discount = (line.discount / 100.0) * line.quantity * line.price_unit
            lines.append({
                "description": line.name,
                "itemType": line.product_id.l10n_eg_item_type if line.product_id.l10n_eg_item_type else "GS1",
                "itemCode": line.product_id.l10n_eg_item_code,
                "unitType": line.product_uom_id.l10n_eg_unit_code,
                "quantity": line.quantity,
                "internalCode": line.product_id.default_code or "",
                "salesTotal": self._get_amount(line.quantity * line.price_unit),
                "total": self._get_amount(self._amount_with_tax(line.price_subtotal, line.tax_ids)),
                "valueDifference": 0,
                "totalTaxableFees": 0,
                "netTotal": self._get_amount(line.price_subtotal),
                "itemsDiscount": 0,
                "unitValue": {
                    "currencySold": self.currency_id.name,
                    "amountEGP": self._get_amount(line.price_unit),
                    "amountSold": 0 if line.price_unit == self._get_amount(
                        line.price_unit) else round(line.price_unit, 5),
                    "currencyExchangeRate": 0 if line.price_unit == self._get_amount(
                        line.price_unit) else self._exchange_currency_rate(),
                },
                "discount": {
                    "rate": line.discount or 0,
                    "amount": discount or 0,
                },
                "taxableItems": [
                    {
                        "taxType": tax.tax_group_id.l10n_eg_tax_code,
                        "amount": self._get_amount(abs((tax.amount / 100.0) * line.price_subtotal)) or 0,
                        "subType": tax.l10n_eg_tax_code,
                        "rate": self._get_amount(abs(tax.amount)) or 0,
                    } for tax in line.tax_ids
                ],
            })
        return lines

    def _get_amount(self, amount):
        from_currency = self.currency_id
        to_currency = self.company_id.currency_id
        new_amount = amount
        if from_currency != to_currency:
            new_amount = from_currency._convert(
                from_amount=amount,
                to_currency=to_currency,
                company=self.company_id,
                date=fields.Date.today(),
                round=False)
        return to_currency.round(new_amount)

    def _exchange_currency_rate(self):
        from_currency = self.currency_id
        to_currency = self.company_id.currency_id
        company = self.company_id
        rate = 1.0
        if from_currency != to_currency:
            rate = self.env['res.currency']._get_conversion_rate(from_currency, to_currency, company,
                                                                 self.invoice_date)
        return to_currency.round(rate)

    def _amount_with_tax(self, amount, tax_ids):
        total_amount = amount
        for tax in tax_ids:
            tax_amount = (tax.amount / 100.0) * amount
            total_amount += tax_amount
        return total_amount
