// odoo.define('l10n_sa_invoice.OrderReceipt', function (require) {
//     'use strict';
//
//     const OrderReceipt = require('point_of_sale.OrderReceipt')
//     const Registries = require('point_of_sale.Registries');
//     const {hooks: {useContext}} = owl;
//
//     class OrderReceiptMod extends OrderReceipt {
//         constructor() {
//             super(...arguments);
//             const order = this.get_order();
//             this.qr_code_ctx = useContext(order.qr_ctx)
//         }
//     }
//     Registries.Component.extend(OrderReceipt, OrderReceiptMod)
//     return OrderReceiptMod
// });
