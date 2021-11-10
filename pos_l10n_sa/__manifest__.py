# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'K.S.A. - Point of Sale',
    'author': 'Odoo S.A',
    'category': 'Accounting/Localizations/Point of Sale',
    'description': """
GCC POS Localization
=======================================================
    """,
    'license': 'LGPL-3',
    'depends': ['pos_l10n_gcc', 'l10n_sa_invoice'],
    'data': [
    ],
    'assets': {
        'web.assets_qweb': [
            'pos_l10n_sa/static/src/xml/OrderReceipt.xml',
        ],
        'point_of_sale.assets': [
            'pos_l10n_sa/static/src/js/lib/qr.js',
            'pos_l10n_sa/static/src/js/OrderReceipt.js',
        ]
    }
}
