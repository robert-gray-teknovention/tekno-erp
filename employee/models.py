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
    phone = models.CharField(max_length=20)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    approvees = models.ManyToManyField("self", blank=True, symmetrical=False, related_name='approvee_set')

    def __str__(self):
        name = self.user.username
        return name
