odoo.define('l10n_sa_invoice.OrderReceipt', function (require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt')
    const Registries = require('point_of_sale.Registries');
    const {hooks: {useContext}} = owl;

    const OrderReceiptMod = x => class extends x {
        constructor() {
            super(...arguments);
            const order = this.env.pos.get_order();
            this.qr_code_ctx = useContext(order.qr_ctx)
        }
        mounted() {
            super.mounted(...arguments);
            var qrcode = new QRCode(document.getElementById("qrcode"), {
                text: this.qr_code_ctx?.qr_base64 ?? "",
                width: 128,
                height: 128,
                colorDark : "#000000",
                colorLight : "#ffffff",
                correctLevel : QRCode.CorrectLevel.H,
                margin: "auto",
            });
        }
    }
    Registries.Component.extend(OrderReceipt, OrderReceiptMod)
    return OrderReceiptMod
});
