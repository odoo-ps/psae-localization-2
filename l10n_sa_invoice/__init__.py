# -*- coding: utf-8 -*-

from . import models
from . import controllers
from odoo.tools import load_language

def install_arabic(cr):
    load_language(cr=cr, lang="ar_001")