from django.contrib import admin
from .models import Employee, TimesheetUser


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'emp_name', 'date_time_in', 'date_time_out', 'duration', 'hourly_rate', 'is_approved')


class TimesheetUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'hourly_rate')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(TimesheetUser, TimesheetUserAdmin)
