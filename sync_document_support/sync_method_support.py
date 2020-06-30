
from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from .frappeclient import FrappeClient
import json
import os
import requests
import subprocess
from frappe.utils.background_jobs import enqueue
from frappe.utils import get_site_name
from frappe.utils import flt, nowdate, add_days, cint





@frappe.whitelist()
def update_received_qty(po_name,prec, sync_site):

	data_so = frappe.db.sql(""" select so.`name` from `tabSales Order` so
		where so.sync_from_document_name  = "{}" """.format(str(po_name)), as_dict = 1)

	if data_so:
		

		docu_so = frappe.get_doc("Sales Order", data_so[0]['name'])

		coba = FrappeClient(sync_site, "sync@mail.com", "asd123")

		docu_prec = coba.get_doc("Purchase Receipt", prec)

		for d in docu_so.items:
			for i in docu_prec["items"]:
				if d.item_code == i["item_code"]:
					d.received_qty += i["received_qty"]



		docu_so.save()


@frappe.whitelist()
def cancel_update_received_qty(po_name,prec, sync_site):

	data_so = frappe.db.sql(""" select so.`name` from `tabSales Order` so
		where so.sync_from_document_name  = "{}" """.format(str(po_name)), as_dict = 1)

	if data_so:
		

		docu_so = frappe.get_doc("Sales Order", data_so[0]['name'])

		coba = FrappeClient(sync_site, "sync@mail.com", "asd123")

		docu_prec = coba.get_doc("Purchase Receipt", prec)

		for d in docu_so.items:
			for i in docu_prec["items"]:
				if d.item_code == i["item_code"]:
					d.received_qty -= i["received_qty"]



		docu_so.save()


@frappe.whitelist()
def validasi_received_qty(doc, method):
	data_so  = frappe.db.sql(""" select distinct(sinv.`sales_order`) as `so` from `tabSales Invoice Item` sinv
		where sinv.`parent` = "{0}" """.format(doc.name), as_dict =1)

	if data_so :
		for d in data_so:
			doc_so = frappe.get_doc("Sales Order", d.so)
			if doc_so.sync_from_document_name:
				for i in doc_so.items:
					if i.delivered_qty != i.received_qty:
						frappe.throw("Jumlah Delivered Quantity item {0} berbeda dengan Received Quantity".format(i.item_code))



