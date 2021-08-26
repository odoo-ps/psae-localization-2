# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    tax_amount = fields.Float(compute="_compute_tax_amount", digits="Product Price")
    tax_ids = fields.Many2many(required=True)

    @api.depends('price_subtotal', 'price_total')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = record.price_total - record.price_subtotal
