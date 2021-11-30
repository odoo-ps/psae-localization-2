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

from flask import Flask, render_template


def _success_action():
    return render_template('success.html')


def _failed_action(error_msg, invoice_id):
    return render_template('failed.html', error_msg=error_msg, invoice_id=invoice_id)
