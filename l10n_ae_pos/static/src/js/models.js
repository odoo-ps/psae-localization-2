odoo.define('l10n_ae_pos_receipt.pos_multi_lang', function (require) {
    "use strict";

    var models = require('point_of_sale.models');

    models.load_models([
        {
            label: 'translations',
            model: 'ir.translation',
            fields: ['value', 'lang', 'src'],
            domain: function (self) {
                let langs = [];
                 _.each(self.langs, function (lang) {
                    if (lang.name === self.config.first_language_id[1] || lang.name === self.config.second_language_id[1]) {
                        langs.push(lang.code);
                    }
                });
                return [
                    ['lang', 'in', langs],
                    '|',
                    ['module', '=', 'l10n_ae_pos'],
                    ['name', '=', 'res.country,vat_label']
                ];
            },
            loaded: function (self, terms) {
                self.translations = {}
                _.each(self.langs, function (lang) {
                    if (lang.name === self.config.first_language_id[1]) {
                        self.translations[lang.code] = {};
                        self.lang_1 = lang.code
                    }
                    if (lang.name === self.config.second_language_id[1]) {
                        self.translations[lang.code] = {};
                        self.lang_2 = lang.code
                    }
                });

                _.each(terms, function (term) {
                    self.translations[term.lang][term.src] = term.value;
                });
            },
        }
    ])

    models.PosModel = models.PosModel.extend({
        translate: function(term_key, lang) {
            if (!this.translations[lang] || !this.translations[lang][term_key]) {
                return term_key;
            }
            return this.translations[lang][term_key];
        },
    })
});