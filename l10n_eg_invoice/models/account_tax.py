# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    l10n_eg_tax_code = fields.Char(help='This is the type of tax according to egyptian tax authority')


class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    l10n_eg_tax_code = fields.Char(help='This is the type of tax group (Parent) according to egyptian tax authority')
