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

import json
import requests
from Redist.result_handle import _success_action, _failed_action
from Redist.config import system_domain

SYSTEM_DOMAIN = system_domain()


def _sign_invoice(sign, invoice_id):
    request_payload = {
        'invoice_id': invoice_id,
        'signatures': sign,
    }
    data = json.dumps(request_payload)
    try:
        request_url = "%s/api/v1/sign_invoice" % (SYSTEM_DOMAIN)
        headers = {'Content-Type': 'application/json'}
        request_response = requests.post(request_url, data=data, headers=headers, verify=False)
        response_data = request_response.json()
    except Exception as ex:
        return _failed_action('%s' % (ex), invoice_id)
    if 'result' in response_data and 'data' in response_data['result']:
        if response_data['result']['data']['result'] == 'Success':
            return _success_action()
    return _failed_action('Document Failed To Sign.', invoice_id)
