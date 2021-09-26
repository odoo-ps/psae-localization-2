# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class Currency(models.Model):
    _inherit = "res.currency"

    currency_unit_label = fields.Char(string="Currency Unit", help="Currency Unit Name", translate=True)
    currency_subunit_label = fields.Char(string="Currency Subunit", help="Currency Subunit Name", translate=True)
