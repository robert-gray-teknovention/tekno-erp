from django.db import models
from timesheets.models import UserTimesheetPeriod


class Invoice(models.Model):
    period = models.OneToOneField(UserTimesheetPeriod, on_delete=models.CASCADE, null=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    date_approved = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)


class InvoiceEntry(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    notes = models.TextField(null=True)
    hourly_rate = models.DecimalField(default=0.00, null=True, decimal_places=2, max_digits=10)
    approver_approved = False
