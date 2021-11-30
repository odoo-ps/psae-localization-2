# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class ProductTemplate(models.AbstractModel):
    _name = 'eta.mixin'

    l10n_eg_code = fields.Char(string='ETA Code (TAX ID)',
                           help='This is the code (TAX ID) of partner according to egyptian tax authority')
    l10n_eg_activity_type = fields.Char('ETA Activity Code',
                                    help='This is the activity type of partner according to egyptian tax authority')
    l10n_eg_building_no = fields.Char('Building No.')
    l10n_eg_floor = fields.Char()
    l10n_eg_room = fields.Char()
    l10n_eg_landmark = fields.Char()
    l10n_eg_additional_information = fields.Char()
