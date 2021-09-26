# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Multi lang POS Receipts",

    'summary':
        """
             This module adds the a second language to the point of sale receipts
         """,

    'description': """
        The receipt will have 3 columns. First column will have the first language name, the second the value, the third the second language name
    """,

    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",

    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'l10n_sa_invoice'],

    # always loaded
    'data': [
        # views
        'views/assets.xml',
        'views/pos_config.xml',
    ],
    'qweb': ['static/src/xml/OrderReceipt.xml'],
}
