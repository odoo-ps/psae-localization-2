# -*- coding: utf-8 -*-
{
    'name': "Egyptian E-Invoice Integration",
    'summary': """
            Egyptian Tax Authority Invoice Integration
        """,
    'description': """
       This module integrate with the ETA Portal to automatically sign and send your invoices to the tax Authority.
    """,
    'author': 'odoo',
    'website': 'https://www.odoo.com',

    'contributors': [
        'Mario Roshdy <marioroshdyn@gmail.com>',
        'Karim Jaber <kareem@plementus.com>'
    ],
    'category': 'account',
    'version': '0.1',
    'depends': ['base', 'account'],
    'data': [
        'data/data.xml',

        'views/account_tax_view.xml',
        'views/product_template_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/uom_uom_view.xml',
        'views/account_move_view.xml',

    ],

}
