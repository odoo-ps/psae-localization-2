# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'U.A.E. - Point of Sale',
    'author': 'Odoo PS',
    'category': 'Accounting/Localizations/Point of Sale',
    'description': """
United Arab Emirates POS Localization
=======================================================
    """,
    'depends': ['point_of_sale'],
    'data': [
        # views
        'views/pos_config.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_ae_pos/static/src/css/pos_receipts.css',
        ],
        'point_of_sale.assets': [
            'l10n_ae_pos/static/src/css/pos_receipts.css',
            'l10n_ae_pos/static/src/js/models.js',
        ],
        'web.assets_qweb': [
            'l10n_ae_pos/static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
        ],
    }
}
