from django.db import models
from employee.models import TimesheetUser
from timesheets.models import TimesheetEntry


class Approval(models.Model):
    timesheet_entry = models.ForeignKey(TimesheetEntry, related_name='approvals', on_delete=models.CASCADE, null=True)
    approver = models.ForeignKey(TimesheetUser, related_name='approver_approvals', on_delete=models.CASCADE, null=True)
    approvee = models.ForeignKey(TimesheetUser, related_name='approvee_approvals', on_delete=models.CASCADE, null=True)
    approval_time = models.DateTimeField(auto_now_add=True)
