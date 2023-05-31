from django.db import models
from timesheets.models import UserTimesheetPeriod


class Invoice(models.Model):
    CREATED = 'CREATED'
    SUBMITTED = 'SUBMITTED'
    APPROVED = 'APPROVED'
    REMITTED = 'REMITTED'
    RECEIVED = 'RECEIVED'
    STATUS_CHOICES = [
        (CREATED, 'Created'),
        (SUBMITTED, 'Submitted'),
        (APPROVED, 'Approved'),
        (REMITTED, 'Remitted'),
        (RECEIVED, 'Received'),
    ]
    period = models.OneToOneField(UserTimesheetPeriod, on_delete=models.CASCADE, null=True)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    date_approved = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    date_remitted = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    date_received = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    amount_remitted = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    received_amount = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CREATED)


class InvoiceEntry(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    notes = models.TextField(null=True)
