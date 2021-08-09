from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    arabic_name = fields.Char(compute="_get_arabic_name", store=True)

    @api.depends("name")
    def _get_arabic_name(self):
        for record in self:
            record.arabic_name = record.with_context(lang="ar_001").name
