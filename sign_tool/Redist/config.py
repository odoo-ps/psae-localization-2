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

TOKEN_PIN = '12345678'
SYSTEM_DOMAIN = 'https://example.com'
SIGN_TOOL_PATH = '/sign/file/path'
SIGNED_DOCUMENT_PATH = '/sign/document/file/path'
CERT_NAME = 'Provider Cert Name'


def token_pin():
    return TOKEN_PIN


def system_domain():
    return SYSTEM_DOMAIN


def sign_tool_path():
    return SIGN_TOOL_PATH


def signed_document_path():
    return SIGNED_DOCUMENT_PATH


def cert_name():
    return CERT_NAME
