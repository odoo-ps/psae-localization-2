odoo.define('pos_l10n_sa.OrderReceipt', function (require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt')
    const Registries = require('point_of_sale.Registries');

    const OrderReceiptQRCodeSA = OrderReceipt =>
        class extends OrderReceipt {
            mounted() {
                super.mounted(...arguments);
                if (this._receiptEnv.order.pos.company.country.code === 'SA') {
                    const qrcode = new QRCode(document.getElementById("qrcode"), {
                        text: this._receiptEnv.receipt?.qr_code ?? "",
                        width: 128,
                        height: 128,
                        colorDark: "#000000",
                        colorLight: "#ffffff",
                        correctLevel: QRCode.CorrectLevel.H,
                        margin: "auto",
                    });
                }
            }

            get receiptEnv() {
                if (this._receiptEnv.order.pos.company.country.code === 'SA') {
                    let receipt_render_env = super.receiptEnv;
                    let receipt = receipt_render_env.receipt;
                    receipt.qr_code = this.compute_sa_qr_code(receipt.company.name, receipt.company.vat, receipt.date.isostring, receipt.total_with_tax, receipt.total_tax);
                    return receipt_render_env;
                }
                return super.receiptEnv;
            }

            compute_sa_qr_code(name, vat, date_isostring, amount_total, amount_tax) {
                /* Generate the qr code for Saudi e-invoicing. Specs are available at the following link at page 23
                https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20210528_ZATCA_Electronic_Invoice_Security_Features_Implementation_Standards_vShared.pdf
                */
                const seller_name_enc = this._compute_qr_code_field(1, name);
                const company_vat_enc = this._compute_qr_code_field(2, vat);
                const timestamp_enc = this._compute_qr_code_field(3, date_isostring);
                const invoice_total_enc = this._compute_qr_code_field(4, amount_total.toString());
                const total_vat_enc = this._compute_qr_code_field(5, amount_tax.toString());

                const str_to_encode = seller_name_enc.concat(company_vat_enc, timestamp_enc, invoice_total_enc, total_vat_enc);

                let binary = '';
                for (let i = 0; i < str_to_encode.length; i++) {
                    binary += String.fromCharCode(str_to_encode[i]);
                }
                return btoa(binary);
            }

            _compute_qr_code_field(tag, field) {
                const company_name_byte_array = this._toUTF8Array(field);
                const company_name_tag_encoding = this._longToByteArray(tag);
                const company_name_length_encoding = this._longToByteArray(company_name_byte_array.length);
                return company_name_tag_encoding.concat(company_name_length_encoding, company_name_byte_array);
            }

            _toUTF8Array(str) {
                // https://stackoverflow.com/questions/18729405/how-to-convert-utf8-string-to-byte-array
                var utf8 = [];
                for (var i = 0; i < str.length; i++) {
                    var charcode = str.charCodeAt(i);
                    if (charcode < 0x80) utf8.push(charcode);
                    else if (charcode < 0x800) {
                        utf8.push(0xc0 | (charcode >> 6),
                            0x80 | (charcode & 0x3f));
                    } else if (charcode < 0xd800 || charcode >= 0xe000) {
                        utf8.push(0xe0 | (charcode >> 12),
                            0x80 | ((charcode >> 6) & 0x3f),
                            0x80 | (charcode & 0x3f));
                    }
                    // surrogate pair
                    else {
                        i++;
                        // UTF-16 encodes 0x10000-0x10FFFF by
                        // subtracting 0x10000 and splitting the
                        // 20 bits of 0x0-0xFFFFF into two halves
                        charcode = 0x10000 + (((charcode & 0x3ff) << 10)
                            | (str.charCodeAt(i) & 0x3ff));
                        utf8.push(0xf0 | (charcode >> 18),
                            0x80 | ((charcode >> 12) & 0x3f),
                            0x80 | ((charcode >> 6) & 0x3f),
                            0x80 | (charcode & 0x3f));
                    }
                }
                return utf8;
            }

            _longToByteArray(long) {
                var bytes = [];
                var i = 8;
                do {
                    bytes[--i] = long & (255);
                    long = long >> 8;
                } while (i)
                return bytes.reverse().slice(0, 1);
            }
        }
    Registries.Component.extend(OrderReceipt, OrderReceiptQRCodeSA)
    return OrderReceiptQRCodeSA
});
