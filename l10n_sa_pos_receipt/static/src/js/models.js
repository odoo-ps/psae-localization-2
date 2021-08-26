odoo.define('l10n_sa_pos_receipt.pos_multi_lang', function (require) {
    "use strict";

    const models = require('point_of_sale.models');
    const {Context} = owl;
    const _order_super = models.Order.prototype;
    const _posmodel_super = models.PosModel.prototype;

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
                    ['module', '=', 'l10n_sa_pos_receipt'],
                    '|',
                    ['module', '=', 'point_of_sale'],
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
        translate: function (term_key, lang) {
            if (!this.translations[lang] || !this.translations[lang][term_key]) {
                return term_key;
            }
            return this.translations[lang][term_key];
        },
    })

    models.Order = models.Order.extend({
        initialize: function () {
            _order_super.initialize.apply(this, arguments);
            this.qr_ctx = new Context({qr_base64: false});
        },
        export_for_printing() {
            const receipt = _order_super.export_for_printing.apply(this, arguments);
            receipt.qr_code = this.qr_ctx.state.qr_base64
            return receipt;
        },
    });

    models.PosModel = models.PosModel.extend({
        _save_to_server: function () {
            /**
             * @override
             * After attempting to save, pass any failing orders to _handle_failed_orders()
             * */
            return _posmodel_super._save_to_server.apply(this, arguments).then(this._add_qr_code.bind(this));
        },
        _add_qr_code: function (server_ids) {
            const finalized_orders = this.get("orders").models.filter(order => order.finalized)
            for (let order of finalized_orders) {
                for (let server_id of server_ids) {
                    if (server_id.pos_reference.includes(order.uid)) {
                        order.qr_ctx.state.qr_base64 = server_id.qr_code_str
                    }
                }
            }
            return server_ids
        },
    });

    models.load_fields("product.product", "arabic_name")
});