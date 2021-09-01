# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, SUPERUSER_ID
from odoo.tools import load_language
from . import models


def pre_init_hook(cr):
    load_language(cr, lang="ar_001")


def post_init_hook(cr, registry):
    load_translations(cr, registry)


def load_translations(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref('l10n_sa.sa_chart_template_standard').process_coa_translations()
