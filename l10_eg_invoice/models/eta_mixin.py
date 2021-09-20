# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class ProductTemplate(models.AbstractModel):
    _name = 'eta.mixin'

    eta_code = fields.Char(string='ETA Code (TAX ID)',
                           help='This is the code (TAX ID) of partner according to egyptian tax authority')
    eta_activity_type = fields.Char('ETA Activity Code',
                                    help='This is the activity type of partner according to egyptian tax authority')
    building_no = fields.Char('Building No.')
    floor = fields.Char()
    room = fields.Char()
    landmark = fields.Char()
    additional_information = fields.Char()
