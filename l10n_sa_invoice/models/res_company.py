# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    secondary_language = fields.Boolean("Enable Secondary Report Language")
    primary_language_code = fields.Many2one("res.lang")
    secondary_language_code = fields.Many2one("res.lang")
    invoice_text = fields.Many2one(comodel_name="report.invoice.lang", string="Invoice Text")
