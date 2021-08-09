# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, SUPERUSER_ID
from . import models


def post_init_hook(cr, registry):
    load_translations(cr, registry)
    link_accounts_to_journals(cr, registry)


def load_translations(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref('l10n_sa.sa_chart_template_standard').process_coa_translations()


def link_accounts_to_journals(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    sa_company_ids = env['res.company'].search([('partner_id.country_id.code', '=', 'SA')]).ids
    zakat_account_codes = ["201019", "400072"]
    ifrs_account_codes = ["100101", "100102", "400070"]
    for sa_company in sa_company_ids:
        ifrs_and_zakat_journals = env['account.journal'].search(
            [('company_id', '=', sa_company), ('code', 'in', ('IFRS', 'ZAKAT'))], limit=2)
        if ifrs_and_zakat_journals[0].code == "IFRS":
            ifrs_journal_id = ifrs_and_zakat_journals[0].id
            zakat_jounral_id = ifrs_and_zakat_journals[1].id
        else:
            ifrs_journal_id = ifrs_and_zakat_journals[1].id
            zakat_jounral_id = ifrs_and_zakat_journals[0].id
        accounts = env['account.account'].search([('company_id', '=', sa_company),
                                                  ('code', 'in', [*zakat_account_codes, *ifrs_account_codes])])
        for account in accounts:
            if account.code in zakat_account_codes:
                account.allowed_journal_ids = [(4, zakat_jounral_id, 0)]
            elif account.code in ifrs_account_codes:
                account.allowed_journal_ids = [(4, ifrs_journal_id, 0)]

def set_accounts_on_tax_groups(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    tax_groups = env['account.tax.group'].search([("name", "in", (env.ref('l10n_sa.sa_tax_group_taxes_15').name, ))])
    tax_groups2 = env['account.tax.group'].search([("id", "=", env.ref('l10n_sa.sa_tax_group_taxes_15').id)])
    import ipdb; ipdb.set_trace()
    taxes_15 = env.ref('l10n_sa.sa_tax_group_taxes_15')
    taxes_15.property_tax_payable_account_id = env.ref("l10n_sa.sa_account_202003")
    taxes_15.property_tax_receivable_account_id= env.ref("l10n_sa.sa_account_100103")
