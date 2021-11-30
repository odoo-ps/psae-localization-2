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
import os
import json
from Redist.result_handle import _failed_action
from Redist.config import token_pin, system_domain, sign_tool_path, signed_document_path, cert_name

TOKEN_PIN = token_pin()
SYSTEM_DOMAIN = system_domain()
SIGN_TOOL_PATH = sign_tool_path()
SIGNED_DOCUMENT_PATH = signed_document_path()
CERT_NAME = cert_name()


def _get_signed_invoice(invoice, invoice_id):
    if 'error' in invoice:
        return _failed_action(invoice['error'], invoice_id)
    json_object = json.dumps(invoice, indent=4)

    res = {}
    try:
        if os.path.exists("%s/SourceDocumentJson.json" % (SIGNED_DOCUMENT_PATH)):
            os.remove("%s/SourceDocumentJson.json" % (SIGNED_DOCUMENT_PATH))
        with open("%s/SourceDocumentJson.json" % (SIGNED_DOCUMENT_PATH), "w", encoding="utf8") as outfile:
            outfile.write(json_object)
    except Exception as ex:
        res.update({
            'error': _failed_action('%s' % (ex), invoice_id)
        })

    try:
        if os.path.exists("%s/FullSignedDocument.json" % (SIGNED_DOCUMENT_PATH)):
            os.remove("%s/FullSignedDocument.json" % (SIGNED_DOCUMENT_PATH))
        if os.path.exists("%s/Cades.txt" % (SIGNED_DOCUMENT_PATH)):
            os.remove("%s/Cades.txt" % (SIGNED_DOCUMENT_PATH))
        if os.path.exists("%s/CanonicalString.txt" % (SIGNED_DOCUMENT_PATH)):
            os.remove("%s/CanonicalString.txt" % (SIGNED_DOCUMENT_PATH))
        os.system(
            "%s %s %s %s" % (SIGN_TOOL_PATH, SIGNED_DOCUMENT_PATH, TOKEN_PIN, '\"' + CERT_NAME + '\"'))
    except Exception as ex:
        res.update({
            'error': _failed_action('%s' % (ex), invoice_id)
        })

    try:

        json_file = open('%s/FullSignedDocument.json' % (SIGNED_DOCUMENT_PATH), "r", encoding="utf8")
        data = json.load(json_file)
    except Exception as ex:
        res.update({
            'error': _failed_action('%s' % (ex), invoice_id)
        })

    if 'error' in res:
        return res
    return {
        'data': data,
    }
