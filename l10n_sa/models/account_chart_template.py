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

    def _load_template(self, company, code_digits=None, account_ref=None, taxes_ref=None):
        account_ref, taxes_ref = super(AccountChartTemplate, self)._load_template(company=company,
                                                                                  code_digits=code_digits,
                                                                                  account_ref=account_ref,
                                                                                  taxes_ref=taxes_ref)
        ifrs_journal = self.env['account.journal'].search(
            [('company_id', '=', company.id), ('code', '=', 'IFRS')]).id
        if ifrs_journal:
            ifrs_account_ids = [self.env.ref('l10n_sa.sa_account_100101').id,
                                self.env.ref('l10n_sa.sa_account_100102').id,
                                self.env.ref('l10n_sa.sa_account_400070').id]
            ifrs_accounts = self.env['account.account'].browse([account_ref.get(id) for id in ifrs_account_ids])
            for account in ifrs_accounts:
                account.allowed_journal_ids = [(4, ifrs_journal, 0)]
        zakat_journal = self.env['account.journal'].search(
            [('company_id', '=', company.id), ('code', '=', 'ZAKAT')]).id
        if zakat_journal:
            zakat_account_ids = [self.env.ref('l10n_sa.sa_account_201019').id,
                                self.env.ref('l10n_sa.sa_account_400072').id]
            zakat_accounts = self.env['account.account'].browse([account_ref.get(id) for id in zakat_account_ids])
            for account in zakat_accounts:
                account.allowed_journal_ids = [(4, zakat_journal, 0)]
        self.env.ref('l10n_sa.sa_tax_group_taxes_15').write(
            {'property_tax_payable_account_id': account_ref.get(self.env.ref('l10n_sa.sa_account_202003').id),
             'property_tax_receivable_account_id': account_ref.get(self.env.ref('l10n_sa.sa_account_100103').id)})
        self.env.ref('l10n_sa.sa_tax_group_taxes_withholding').write(
            {'property_tax_payable_account_id': account_ref.get(self.env.ref('l10n_sa.sa_account_201020').id),
             'property_tax_receivable_account_id': account_ref.get(self.env.ref('l10n_sa.sa_account_201020').id)}) # Get correct account from Nada
        return account_ref, taxes_ref

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
