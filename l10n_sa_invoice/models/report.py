# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class Report(models.Model):
    _name = "report.invoice.lang"
    _description = "Translation for dual language invoices"

    name = fields.Char("Name")
    posted = fields.Char("Invoice", default="Invoice", translate=True)
    draft = fields.Char("Draft Invoice", default="Draft Invoice", translate=True)
    cancel = fields.Char("Cancelled Invoice", default="Cancelled Invoice", translate=True)
    out_refund = fields.Char("Credit Note", default="Credit Note", translate=True)
    in_refund = fields.Char("Vendor Credit Note", default="Vendor Credit Note", translate=True)
    in_invoice = fields.Char("Vendor Bill", default="Vendor Bill", translate=True)
    invoice_date = fields.Char("Invoice Date", default="Invoice Date", translate=True)
    due_date = fields.Char("Due Date", default="Due Date", translate=True)
    delivery_date = fields.Char("Delivery Date", default="Delivery Date", translate=True)
    source = fields.Char("Source", default="Source", translate=True)
    customer_code = fields.Char("Customer Code", default="Customer Code", translate=True)
    reference = fields.Char("Reference", default="Reference", translate=True)
    description = fields.Char("Description", default="Description", translate=True)
    source_document = fields.Char("Source Document", default="Source Document", translate=True)
    quantity = fields.Char("Quantity", default="Quantity", translate=True)
    unit_price = fields.Char("Unit Price", default="Unit Price", translate=True)
    discount_percent = fields.Char("Discount (%)", default="Discount (%)", translate=True)
    taxes = fields.Char("Total Vat", default="Total Vat", translate=True)
    amount = fields.Char("Taxable Amount", default="Taxable Amount", translate=True)
    price = fields.Char("Price", default="Price", translate=True)
    subtotal = fields.Char("Subtotal", default="Subtotal Subject to VAT", translate=True)
    total = fields.Char("Total", default="Total", translate=True)
    amount_due = fields.Char("Amount Due", default="Amount Due", translate=True)
    payment_reference = fields.Char("Payment Reference Line",
                                    default="Please use the following communication for your payment", translate=True)
    total_price = fields.Char('Total including VAT', default="Total including VAT", translate=True)
    tax_id = fields.Char("VAT Number", default="Tax ID", translate=True)
    paid_on = fields.Char("Paid on", default="Paid on", translate=True)
    amount_due_in_words = fields.Char("Amount Due in words", default="Amount Due in words", translate=True)
    incoterm = fields.Char("Incoterm", default="Incoterm", translate=True)
    tax_amount = fields.Char("Tax Amount", default="Tax Amount", translate=True)
