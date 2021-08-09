from odoo import models, api, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    font = fields.Selection(selection_add=[('Tajawal', 'Tajawal'), ('Amiri', 'Amiri'), ('Mirza', 'Mirza'),
                                           ('Markazi_Text', 'Markazi+Text')])
