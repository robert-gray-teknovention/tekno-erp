from django.db import models
from employee.models import TimesheetUser


class TimesheetEntry(models.Model):
    user = models.ForeignKey(TimesheetUser, on_delete=models.CASCADE)
    date_time_entry = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_time_in = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_time_out = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        name = self.user.first_name + ' ' + self.user.last_name
        return name
