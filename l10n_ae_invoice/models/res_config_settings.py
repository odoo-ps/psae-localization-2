# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dual_invoice_language = fields.Boolean(related='company_id.dual_invoice_language', store=True, readonly=False)
