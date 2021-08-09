# -*- coding: utf-8 -*-
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

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        # views
        'views/assets.xml',
        'views/pos_config.xml',
    ],
    'qweb': ['static/src/xml/OrderReceipt.xml'],
    # only loaded in demonstration mode
    'demo': [],
}
