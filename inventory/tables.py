import django_tables2 as tables
from .models import (InventoryItem, InventoryFood)
from purchasing.models import Item
from django.utils.html import format_html


class ItemTable(tables.Table):
    
    def render_name(self, value, record):
        return format_html("<b><a href='../item/{}/item/{}/'>{}</a></b>", record.__class__.__name__.lower(), record.id, value)
        # return fromat_html("<b><a href=''></a></b>")
    
    def render_inventory_quantities(self, value, record):
        return format_html("<b><a href='#'>{}</a></b>", value)

    class Meta:
        model = Item
        sequence = ("name", "description")
        exclude = ("id", "organization", "polymorphic_ctype")


class PartTable(ItemTable):
    inventory_quantities = tables.Column(accessor='get_inventory_quantity')


class MaterialTable(ItemTable):
    inventory_quantities = tables.Column(accessor='get_inventory_quantity')


class FoodTable(ItemTable):
    inventory_quantities = tables.Column(accessor='get_inventory_quantity')


class InventoryItemTable(tables.Table):
    def render_location(self, value, record):
        return format_html("<b><a href='#' onclick='loadInventoryItemFormEdit({})'>{}</a></b>", record.id, record.location)

    class Meta:
        model = InventoryItem
        exclude = ("id", )
        sequence = ("location", "quantity", "units",)
        
