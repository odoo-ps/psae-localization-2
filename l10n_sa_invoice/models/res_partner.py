from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    name = fields.Char(translate=True)
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    zip = fields.Char(translate=True)
    city = fields.Char(translate=True)
