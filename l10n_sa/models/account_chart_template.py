# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api


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

    def _load(self, sale_tax_rate, purchase_tax_rate, company):
        super(AccountChartTemplate, self)._load(sale_tax_rate=sale_tax_rate, purchase_tax_rate=purchase_tax_rate,
                                                company=company)
        company.default_cash_difference_expense_account_id.with_context(lang='ar_001').name = 'خسارة الفرق النقدي'
        company.default_cash_difference_income_account_id.with_context(lang='ar_001').name = 'مكاسب الفرق النقدي'
        return {}

    @api.model
    def _create_liquidity_journal_suspense_account(self, company, code_digits):
        account = super(AccountChartTemplate, self)._create_liquidity_journal_suspense_account(company=company,
                                                                                               code_digits=code_digits)
        account.with_context(lang='ar_001').name = 'حساب البنك المعلق'
        return account
