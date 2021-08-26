# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tools import load_language
from . import models


def install_arabic(cr):
    load_language(cr=cr, lang="ar_001")
