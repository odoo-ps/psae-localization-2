from odoo import models, fields


class HREmployee(models.Model):
    _inherit = "hr.employee"

    end_employment = fields.Boolean()
    end_of_service = fields.Boolean()
