# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Saudi Arabia - Dual Language Invoice',
    'version': '14.0.1.0.0',
    'author': 'Odoo PS',
    'category': 'Accounting/Localizations',
    'description': """
    Dual Language Invoice for Saudi Arabia
""",
    'depends': ['account', 'arabic_friendly_fonts'],
    'data': [
        'security/ir.model.access.csv',
        'data/report_invoice_lang.xml',
        'views/view_move_form.xml',
        'views/report_invoice.xml',
        'views/res_config_settings_views.xml',
        'views/report_dual_language_invoice.xml',
    ],
    # 'pre_init_hook': 'install_arabic',
}
