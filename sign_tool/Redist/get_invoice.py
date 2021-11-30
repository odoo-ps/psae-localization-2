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
from Redist.config import system_domain

SYSTEM_DOMAIN = system_domain()


def _get_invoice(invoice_id):
    request_payload = {
        'invoice_id': invoice_id
    }
    data = json.dumps(request_payload)
    try:
        request_url = "%s/api/v1/get_invoice" % (SYSTEM_DOMAIN)
        headers = {'Content-Type': 'application/json'}
        request_response = requests.post(request_url, data=data, headers=headers, verify=False)
        response_data = request_response.json()
        if 'result' in response_data and 'data' in response_data['result']:
            invoice = response_data['result']['data']
            return invoice
        return {'error': 'Cannot Access The Document'}
    except Exception as ex:
        return {'error': '%s' % (ex)}
