from odoo import models


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _prepare_all_journals(self, acc_template_ref, company, journals_dict=None):
        """ If Saudi Arabia chart, we add 3 new journals Tax Adjustments, IFRS 16 and Zakat"""
        if company.country_id.code == "SA":
            if not journals_dict:
                journals_dict = []
            journals_dict.extend(
                [{"name": "Tax Adjustments", "company_id": company.id, "code": "TA", "type": "general",
                  "favorite": True, "sequence": 1},
                 {"name": "IFRS 16 Right of Use Asset", "company_id": company.id, "code": "IFRS", "type": "general",
                  "favorite": True, "sequence": 10},
                 {"name": "Zakat", "company_id": company.id, "code": "ZAKAT", "type": "general", "favorite": True,
                  "sequence": 10}])
        return super()._prepare_all_journals(acc_template_ref, company, journals_dict=journals_dict)
