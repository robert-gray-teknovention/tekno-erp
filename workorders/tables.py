import django_tables2 as tables
from django.utils.html import format_html
from .models import WorkOrder, WorkEntry


class WorkOrderTable(tables.Table):
    assigned_to = tables.Column(default="None")
    
    def render_request(self, value, record):
        # Link the request text to the edit page for the workorder
        short = (value[:75] + '...') if value and len(value) > 75 else (value or "")
        return format_html("<a href='{}'>{}</a>", f"/workorders/{record.id}/", short)

    def render_assigned_to(self, value, record):
        # Join M2M assigned_to display names
        return ", ".join([str(u) for u in record.assigned_to.all()])

    actions = tables.TemplateColumn(
        "<a href='/workorders/{{record.id}}/edit/' class='btn btn-sm btn-outline-primary me-1'>Edit</a>"
        "<a href='/workorders/{{record.id}}/delete/' class='btn btn-sm btn-outline-danger'>Delete</a>",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = WorkOrder
        sequence = ("create_date", "project", "equipment", "status", "assigned_to", "request", "actions")
        exclude = ("notes", "is_active", "creator")


class WorkEntryTable(tables.Table):
    def render_work_order(self, value, record):
        if value:
            return format_html("<a href='{}'>WO #{}</a>", f"/workorders/{value.id}/edit/", value.id)
        return ""

    def render_user(self, value, record):
        return str(value)

    actions = tables.TemplateColumn(
        "<a href='/workorders/workentries/{{record.id}}/edit/?next=/workorders/{{record.work_order.id}}/' class='btn btn-sm btn-outline-primary me-1'>Edit</a>"
        "<a href='/workorders/workentries/{{record.id}}/delete/?next=/workorders/{{record.work_order.id}}/' class='btn btn-sm btn-outline-danger'>Delete</a>",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = WorkEntry
        sequence = ("user", "date_time_in", "duration", "project", "work_order", "actions")
        exclude = ("docs", "approver_approved", "period", "hourly_rate")
