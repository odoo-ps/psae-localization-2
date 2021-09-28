# -*- coding: utf-8 -*-
{
    'name': "Arabic fonts",

    'description': """
        Custom fonts for arabic characters
    """,

    'author': "Odoo sa",
    'website': "http://www.odoo.com",

    'category': 'user',
    'version': '1',

    'depends': [
        'base', 'web'
    ],
    'assets': {
        'web.assets_common': [
            'l10n_ae_font/static/src/scss/fonts.scss',
        ],
        'web.report_assets_common': [
            'l10n_ae_font/static/src/scss/fonts.scss',
        ],
    }
}
