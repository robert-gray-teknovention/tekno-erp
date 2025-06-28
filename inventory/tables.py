import django_tables2 as tables
from .models import (InventoryPart, InventoryMaterial)
from django.utils.html import format_html


class InventoryPartTable(tables.Table):
    def render_name(self, value, record):
        return format_html("<b><a href='../part/update/{}/{}?url=list'>{}</a></b>", record.__class__.__name__, record.id, value)

    class Meta:
        model = InventoryPart
        sequence = ("part.name", "part.description", "quantity")
        
