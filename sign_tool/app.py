##############################################################################
#
#
#    Copyright (C) 2019-TODAY .
#    Author: Plementus <https://plementus.com>
#    Contributor: Mario Roshdy <m.roshdy@plementus.com>
#    Contributor: Karim Jaber <kareem@plementus.com>
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
##############################################################################

from flask import Flask, render_template, request, redirect
from Redist.config import token_pin, system_domain, sign_tool_path, signed_document_path
from Redist.get_sign import _get_sign
from Redist.result_handle import _failed_action

app = Flask(__name__)
TOKEN_PIN = token_pin()
SYSTEM_DOMAIN = system_domain()
SIGN_TOOL_PATH = sign_tool_path()
SIGNED_DOCUMENT_PATH = signed_document_path()


@app.route('/', methods=['GET'])
def login():
    invoice_id = request.args.get('invoice_id')
    if not invoice_id:
        return "Not valid invoice ID"
    return render_template('login.html', invoice_id=invoice_id)


@app.route('/get_sign', methods=['POST'])
def get_sign():
    pin = request.form.get('pin')
    invoice_id = request.form.get('invoice_id')
    if invoice_id == 'undefined':
        return _failed_action('Undefined Document ID Assigned.')
    if str(pin) != TOKEN_PIN:
        return _failed_action('PIN is not correct.', invoice_id)
    return _get_sign(invoice_id)


if __name__ == '__main__':
    app.run(port=5100)
