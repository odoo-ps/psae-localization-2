from odoo import api, models, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def _fill_missing_values(self, vals):
        journal_type = vals.get('type')

        # 'type' field is required.
        if not journal_type:
            return

        # === Fill missing company ===
        company = self.env['res.company'].browse(vals['company_id']) if vals.get('company_id') else self.env.company
        vals['company_id'] = company.id

        # Don't get the digits on 'chart_template_id' since the chart template could be a custom one.
        random_account = self.env['account.account'].search([('company_id', '=', company.id)], limit=1)
        digits = len(random_account.code) if random_account else 6

        liquidity_type = self.env.ref('account.data_account_type_liquidity')
        current_assets_type = self.env.ref('account.data_account_type_current_assets')

        if journal_type in ('bank', 'cash'):
            has_liquidity_accounts = vals.get('default_account_id')
            has_payment_accounts = vals.get('payment_debit_account_id') or vals.get('payment_credit_account_id')
            has_profit_account = vals.get('profit_account_id')
            has_loss_account = vals.get('loss_account_id')

            if journal_type == 'bank':
                liquidity_account_prefix = company.bank_account_code_prefix or ''
            else:
                liquidity_account_prefix = company.cash_account_code_prefix or company.bank_account_code_prefix or ''

            # === Fill missing name ===
            vals['name'] = vals.get('name') or vals.get('bank_acc_number')

            # === Fill missing code ===
            if 'code' not in vals:
                vals['code'] = self.get_next_bank_cash_default_code(journal_type, company)
                if not vals['code']:
                    raise UserError(_("Cannot generate an unused journal code. Please fill the 'Shortcode' field."))

            # === Fill missing accounts ===
            if not has_liquidity_accounts:
                default_account_code = self.env['account.account']._search_new_account_code(company, digits,
                                                                                            liquidity_account_prefix)
                default_account_vals = self._prepare_liquidity_account_vals(company, default_account_code, vals)
                # Custom code starts: SAL
                default_account = self.env['account.account'].create(default_account_vals)
                if default_account_vals.get('name') == 'Cash':
                    default_account.with_context(lang='ar_001').name = 'النقد'
                elif default_account_vals.get('name') == 'Bank':
                    default_account.with_context(lang='ar_001').name = 'البنك'
                vals['default_account_id'] = default_account.id
            if not has_payment_accounts:
                payment_debit_account = self.env['account.account'].create({
                    'name': _("Outstanding Receipts"),
                    'code': self.env['account.account']._search_new_account_code(company, digits,
                                                                                 liquidity_account_prefix),
                    'reconcile': True,
                    'user_type_id': current_assets_type.id,
                    'company_id': company.id,
                })
                payment_debit_account.with_context(lang='ar_001').name = 'الإيصالات المعلقة'
                vals['payment_debit_account_id'] = payment_debit_account.id
                payment_credit_account = self.env['account.account'].create({
                    'name': _("Outstanding Payments"),
                    'code': self.env['account.account']._search_new_account_code(company, digits,
                                                                                 liquidity_account_prefix),
                    'reconcile': True,
                    'user_type_id': current_assets_type.id,
                    'company_id': company.id,
                })
                payment_credit_account.with_context(lang='ar_001').name = 'المدفوعات المستحقة'
                vals['payment_credit_account_id'] = payment_credit_account.id
                # Custom code ends: SAL
            if journal_type == 'cash' and not has_profit_account:
                vals['profit_account_id'] = company.default_cash_difference_income_account_id.id
            if journal_type == 'cash' and not has_loss_account:
                vals['loss_account_id'] = company.default_cash_difference_expense_account_id.id

        # === Fill missing refund_sequence ===
        if 'refund_sequence' not in vals:
            vals['refund_sequence'] = vals['type'] in ('sale', 'purchase')
