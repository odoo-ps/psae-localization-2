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

from Redist.get_invoice import _get_invoice
from Redist.get_signed_invoice import _get_signed_invoice
from Redist.sign_invoice import _sign_invoice
from Redist.result_handle import _failed_action


def _get_sign(invoice_id):
    invoice = _get_invoice(invoice_id)
    res = _get_signed_invoice(invoice, invoice_id)
    if 'error' in res:
        return res['error']
    data = res['data']
    sign = 'False'
    if data and 'documents' in data:
        sign = data['documents'][0]['signatures']
        if sign and len(sign[0]['value']) > 100:
            return _sign_invoice(sign, invoice_id)
    return _failed_action('Document Failed To Sign', invoice_id)
