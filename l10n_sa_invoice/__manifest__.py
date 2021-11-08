# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'K.S.A. - Arabic/English Invoice',
    'version': '1.0.0',
    'author': 'Odoo',
    'category': 'Accounting/Localizations',
    'description': """
    Arabic/English for the kingdom of Saudi Arabia
""",
    'license': 'LGPL-3',
    'depends': ['account', 'l10n_ae_invoice'],
    'data': [
        'views/view_move_form.xml',
        'views/report_invoice.xml',
    ],
}
