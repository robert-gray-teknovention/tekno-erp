import django_tables2 as tables
from django.utils.html import format_html
from .models import WorkOrder, WorkEntry


class WorkOrderTable(tables.Table):
    assigned_to = tables.Column(default="None")
    
    def render_request(self, value, record):
        # Link the request text to the edit page for the workorder
        short = (value[:75] + '...') if value and len(value) > 75 else (value or "")
        return format_html("<a href='{}' data-work-order-id='{}'>{}</a>", f"/workorders/{record.id}/", record.id, short)

    def render_assigned_to(self, value, record):
        # Join M2M assigned_to display names
        return ", ".join([str(u) for u in record.assigned_to.all()])

    actions = tables.TemplateColumn(
        "<a href='/workorders/{{record.id}}/delete/' class='btn btn-sm btn-outline-danger'>Delete</a>",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = WorkOrder
        sequence = ("id", "create_date", "project", "equipment", "status", "assigned_to", "request", "actions")
        exclude = ("notes", "is_active", "creator", "start_date", "end_date", "scheduled_at")

class WorkOrderListTable(tables.Table):
    select = tables.TemplateColumn(
        template_code="<input type='radio' name='work_order' value='{{record.id}}'>",
        verbose_name="Select",
        orderable=False,
    )

    class Meta:
        model = WorkOrder
        fields = ("select", "id", "create_date", "project", "equipment", "status", "assigned_to", "request")

class WorkEntryTable(tables.Table):
    def render_notes(self, value, record):
        if value:
            return format_html("<a href='/workorders/workentries/{}/edit/?next=/workorders/{}/'>​{}</a>", record.id, record.work_order.id, value)
        return ""

    def render_user(self, value, record):
        return str(value)

    actions = tables.TemplateColumn(
        "<a href='/workorders/workentries/{{record.id}}/delete/?next=/workorders/{{record.work_order.id}}/' class='btn btn-sm btn-outline-danger'>Delete</a>",
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = WorkEntry
        sequence = ("id", "date_time_in", "date_time_out", "duration", "project", "notes", "actions")
        exclude = ("docs", "approver_approved", "period", "hourly_rate", "timesheetentry_ptr", "is_approved", "user", "date_time_entry ", "work_order", "date_time_entry")
