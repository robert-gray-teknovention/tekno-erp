import django_tables2 as tables
from .models import Vendor, Manufacturer, PurchaseOrder, PurchaseOrderItem
from django.utils.html import format_html


class VendorTable(tables.Table):
    def render_name(self, value, record):
        return format_html("<b><a href='company?v_id={}&type=vendor'>{}</a></b>", record.id, value)

    class Meta:
        model = Vendor
        sequence = ("name", "website", "email", "phone")
        exclude = ("id", "organization")


class ManufacturerTable(tables.Table):
    def render_name(self, value, record):
        return format_html("<b><a href='company?v_id={}&type=manufacturer'>{}</a></b>", record.id, value)

    class Meta:
        model = Manufacturer
        sequence = ("name", "website", "email", "phone")
        exclude = ("id", "organization")


class PurchaseOrderTable(tables.Table):
    def render_create_date(self, value, record):
        return format_html("<b><a href='../purchaseorder/{}/update/'>{}</a></b>", record.id, value.strftime("%m-%d-%Y %I:%M %p"))

    class Meta:
        model = PurchaseOrder
        sequence = ("id", "create_date", "vendor", "orderer")
        exclude = ("organization", "purchaser", "sub_total", "shipping", "tax")


class PurchaseOrderItemTable(tables.Table):

    class Meta:
        model = PurchaseOrderItem
        sequence = ("purchase_item", "quantity")
        exclude = ("purchase_order", "id", "status_change_date")
