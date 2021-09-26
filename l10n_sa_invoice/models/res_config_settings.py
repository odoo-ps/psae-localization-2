# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    secondary_language = fields.Boolean(string="Enable Secondary Report Language",
                                        related="company_id.secondary_language", store=True, readonly=False)
    primary_language_code = fields.Many2one(comodel_name="res.lang", string="Primary Language",
                                            related="company_id.primary_language_code", store=True, readonly=False)
    secondary_language_code = fields.Many2one(comodel_name="res.lang", string="Secondary Language",
                                              related="company_id.secondary_language_code", store=True, readonly=False)
    invoice_text = fields.Many2one(comodel_name="report.invoice.lang", related="company_id.invoice_text", store=True,
                                   readonly=False)
