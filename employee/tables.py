import django_tables2 as tables
from .models import Invitee


class InviteeTable(tables.Table):
    class Meta:
        model = Invitee
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "email", "wage", "status", "status_date")
