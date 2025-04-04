import django_tables2 as tables
from django.utils.html import format_html
from .models import Project


class ProjectTable(tables.Table):
    def render_name(self, value, record):
        print("val ", value, "record ", str(record.id))
        return format_html("<b><a href='../project/{}/update/'>{}</a></b>", record.id, value)

    class Meta:
        model = Project
        sequence = ("name", "description")
        exclude = ("id", "start_date", "finished_date")
