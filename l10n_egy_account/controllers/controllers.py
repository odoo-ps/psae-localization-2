# -*- coding: utf-8 -*-
# from odoo import http


# class L10nEgyAccount(http.Controller):
#     @http.route('/l10n_egy_account/l10n_egy_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_egy_account/l10n_egy_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_egy_account.listing', {
#             'root': '/l10n_egy_account/l10n_egy_account',
#             'objects': http.request.env['l10n_egy_account.l10n_egy_account'].search([]),
#         })

#     @http.route('/l10n_egy_account/l10n_egy_account/objects/<model("l10n_egy_account.l10n_egy_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_egy_account.object', {
#             'object': obj
#         })
