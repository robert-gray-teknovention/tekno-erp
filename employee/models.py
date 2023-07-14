from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization


# Create your models here.
class Employee(models.Model):
    emp_id = models.IntegerField(blank=True)
    emp_name = models.CharField(max_length=255)
    date_time_in = models.CharField(max_length=255)
    date_time_out = models.CharField(max_length=255)
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.emp_name


class TimesheetUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    approvers = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='approvees')
    org_manager = models.ManyToManyField(Organization, blank=True, related_name='managers')

    def __str__(self):
        name = self.user.username
        return name


class Invitee(models.Model):
    class Status(models.TextChoices):
        INVITED = 'INVITED', 'Invited'
        REGISTERED = 'REGISTERED', 'Registered'
        ACTIVATED = 'ACTIVATED', 'Activated'

    name = models.CharField(max_length=75, default='')
    user = models.OneToOneField(TimesheetUser, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=75)
    authentication_code = models.CharField(max_length=15)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.INVITED)
    status_date = models.DateTimeField(auto_now=True)
    wage = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)
    inviter = models.ForeignKey(TimesheetUser, on_delete=models.SET_NULL, null=True, related_name='inviter')

    class Meta:
        permissions = (
            ('invite', 'Can invite new user'),
            ('uninvite', 'Can uninvite an invitee')
        )
