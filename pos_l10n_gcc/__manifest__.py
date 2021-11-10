# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'G.C.C. - Point of Sale',
    'author': 'Odoo S.A',
    'category': 'Accounting/Localizations/Point of Sale',
    'description': """
GCC POS Localization
=======================================================
    """,
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
    ],
    'assets': {
        'web.assets_qweb': [
            'pos_l10n_gcc/static/src/xml/OrderReceipt.xml',
        ],
        'point_of_sale.assets': [
            'pos_l10n_gcc/static/src/js/OrderReceipt.js',
        ]
    }
}
