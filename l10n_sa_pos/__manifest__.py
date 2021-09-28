# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "K.S.A. - Point of Sale",

    'category': 'Accounting/Localizations/Point of Sale',
    'description': """
Kingdom of Saudi Arabia POS Localization
=======================================================
        """,

    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",

    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'l10n_sa_invoice', 'l10n_ae_pos'],
    'assets': {
        'web.assets_backend': [
            'l10n_sa_pos/static/src/js/qr.js',
        ],
        'point_of_sale.assets': [
            'l10n_sa_pos/static/src/css/pos_receipt.css',
            'l10n_sa_pos/static/src/js/qr.js',
            'l10n_sa_pos/static/src/js/models.js',
            'l10n_sa_pos/static/src/js/Screens/ReceiptScreen/OrderReceipt.js',
        ],
        'web.assets_qweb': [
            'l10n_sa_pos/static/src/xml/OrderReceipt.xml',
        ],
    }
}
