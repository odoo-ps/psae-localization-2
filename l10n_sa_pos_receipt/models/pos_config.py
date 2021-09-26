# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class PosConfig(models.Model):
    _inherit = 'pos.config'

    two_language_receipt = fields.Boolean()
    first_language_id = fields.Many2one('res.lang')
    second_language_id = fields.Many2one('res.lang')
    text_field = fields.Char()
