import django_tables2 as tables
from .models import Vendor, Manufacturer
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
