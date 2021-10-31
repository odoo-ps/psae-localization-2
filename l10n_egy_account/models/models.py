# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _inherit = 'account.account'
    name = fields.Char(translate=True)


class Journals(models.Model):
    _inherit = 'account.journal'
    name = fields.Char(translate=True)


class Tax(models.Model):
    _inherit = 'account.tax'
    name = fields.Char(translate=True)


class AccountTaxReport(models.Model):
    _inherit = "account.tax.report"

    name = fields.Char(translate=True)

class AccountTaxReportLine(models.Model):
    _inherit = "account.tax.report.line"

    name = fields.Char(translate=True)
    tag_name = fields.Char(translate=True)