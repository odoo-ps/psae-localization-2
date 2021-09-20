# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields, api


class ResCompany(models.Model):
    _name = 'res.company'
    _inherit = ['res.company', 'eta.mixin']

    eta_client_identifier = fields.Char('ETA Client ID')
    eta_client_secret_1 = fields.Char()
    eta_client_secret_2 = fields.Char()
    eta_branch_identifier = fields.Char('ETA Branch ID')
