import logging

from odoo import models, tools, _, fields
from odoo.tools.misc import get_lang

_logger = logging.getLogger(__name__)
try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class Currency(models.Model):
    _inherit = "res.currency"

    currency_unit_label = fields.Char(string="Currency Unit", help="Currency Unit Name", translate=True)
    currency_subunit_label = fields.Char(string="Currency Subunit", help="Currency Subunit Name", translate=True)

    def amount_to_text_custom(self, amount, input_lang=None):
        self.ensure_one()

        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)

        if not input_lang:
            lang_code = self.env.context.get('lang') or self.env.user.lang or get_lang(self.env).code
        else:
            lang_code = input_lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
            amt_value=_num2words(integer_value, lang=lang.iso_code),
            amt_word=self.currency_unit_label,
        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + ('and' if input_lang else _('and')) + tools.ustr(' {amt_value} {amt_word}').format(
                amt_value=_num2words(fractional_value, lang=lang.iso_code),
                amt_word=self.currency_subunit_label,
            )
        return amount_words
