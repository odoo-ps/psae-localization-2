# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class UomUom(models.Model):
    _inherit = 'uom.uom'

    l10n_eg_unit_code = fields.Char(help='This is the type of unit according to egyptian tax authority')
