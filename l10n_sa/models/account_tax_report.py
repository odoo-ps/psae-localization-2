# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class AccountTaxReport(models.Model):
    _inherit = "account.tax.report"

    name = fields.Char(translate=True)
