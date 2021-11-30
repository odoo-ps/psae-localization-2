odoo.define('eta_einvoice_integration.sign_invoice', function (require) {
"use strict";

var Widget = require('web.Widget');
var core = require('web.core');
var _t = core._t;
var QWeb = core.qweb;

var framework = require('web.framework');
var form_widget = require('web.FormRenderer');
form_widget.include({
    _addOnClickAction: function ($el, node) {
        if(node.attrs.name === "action_post_sign_invoice"){
            var self = this;
            $el.click(function (e) {
                self._rpc({
                    model: 'account.move',
                    method: 'get_default_sign_host',
                    args: []
                }).then(function (res) {
                    var invoice_id = self.state.res_id;
                    var sign_host = res
    //                var win = window.open("http://localhost:5100?invoice_id="+invoice_id, "_blank", "height=500,width=400");
    //                 alert(sign_host)
                    var win = window.open(sign_host+"?invoice_id="+invoice_id, "_blank", "height=500,width=400");
                    if (win){
                        e.preventDefault();
                    }
                    var pollTimer = window.setInterval(function() {
                        if (win.closed !== false) {
                            window.clearInterval(pollTimer);
                            self.trigger_up('reload');
                        }
                    }, 200);
                });
            });
        }else{
            if (node.attrs.special || node.attrs.confirm || node.attrs.type || $el.hasClass('oe_stat_button')) {
                var self = this;
                $el.click(function () {
                    self.trigger_up('button_clicked', {
                        attrs: node.attrs,
                        record: self.state,
                    });
                });
            }
        }
    },
});

});
