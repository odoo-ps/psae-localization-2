from odoo import fields, models


class CountryState(models.Model):
    _inherit = 'res.country.state'
    _order = 'code'

    name = fields.Char(translate=True)
    code = fields.Char(translate=True)