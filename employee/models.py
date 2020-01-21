from django.db import models
from datetime import datetime


# Create your models here.
class Employee(models.Model):
    emp_id = models.IntegerField(blank=True)
    emp_name = models.CharField(max_length=255)
    date_time_in = models.CharField(max_length=255)
    date_time_out = models.CharField(max_length=255)
    duration = models.FloatField()
    hourly_rate = models.FloatField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.emp_name

