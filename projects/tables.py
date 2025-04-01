import django_tables2 as tables
from django.utils.html import format_html
from .models import Project


class ProjectTable(tables.Table):
    def render_name(self, value, record):
        return format_html("<b><a href='../project/update/{}/{}?url=list'>{}</a></b>", record.__class__.__name__,
                           record.id, value)

    class Meta:
        model = Project
        sequence = ("name", "description")
        exclude = ("id")
