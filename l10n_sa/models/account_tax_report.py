from odoo import models, fields


class AccountTaxReport(models.Model):
    _inherit = "account.tax.report"

    name = fields.Char(translate=True)
