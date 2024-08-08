from django.db import models
from employee.models import TimesheetUser
from organizations.models import Organization
from projects.models import Project

class TimesheetPeriod(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False)
    date_start = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_end = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        unique_together = ('org_id', 'date_start', 'date_end')
        permissions = (('approve_timesheetperiod', 'can approve timesheetperiod'),)

    def __str__(self):
        return_string = str(self.date_start.month) + '/' + str(self.date_start.day) + '/'
        return_string += str(self.date_start.year) + ' - '
        return_string += str(self.date_end.month) + '/' + str(self.date_end.day) + '/' + str(self.date_end.year)
        return return_string


class TimesheetEntry(models.Model):
    user = models.ForeignKey(TimesheetUser, on_delete=models.CASCADE)
    date_time_entry = models.DateTimeField(auto_now_add=True)
    date_time_in = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_time_out = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    period = models.ForeignKey(TimesheetPeriod, on_delete=models.CASCADE, null=True)
    notes = models.TextField(null=True)
    hourly_rate = models.DecimalField(default=0.00, null=True, decimal_places=2, max_digits=10)
    approver_approved = False
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        #        name = self.user.first_name + ' ' + self.user.last_name
        name = str(self.date_time_in) + str(self.project)
        return name

    class Meta:
        permissions = (("approve_timesheetentry", "can approve timesheetentry"),)


class UserTimesheetPeriod(models.Model):
    user = models.ForeignKey(TimesheetUser, on_delete=models.CASCADE)
    period = models.ForeignKey(TimesheetPeriod, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    date_approved = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    entries = []

    class Meta:
        unique_together = ('user', 'period')

    def __str__(self):
        return_string = str(self.user) + ' ' + str(self.period)
        return return_string
