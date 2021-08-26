# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class CountryState(models.Model):
    _inherit = 'res.country.state'
    _order = 'code'

    name = fields.Char(translate=True)
    code = fields.Char(translate=True)
