from django.contrib import admin
from .models import Employee, TimesheetUser, AlternateWageCode


class ApproveesInLine(admin.TabularInline):
    model = TimesheetUser.approvees.through
    extra = 1
    fk_name = "from_timesheetuser"


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'emp_name', 'date_time_in', 'date_time_out', 'duration', 'hourly_rate', 'is_approved')


class TimesheetUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'hourly_rate')
    inlines = [
        ApproveesInLine,
    ]


class AlternateWageCodeAdmin(admin.ModelAdmin):
    list_display = ('hourly_rate', 'description')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(TimesheetUser, TimesheetUserAdmin)
admin.site.register(AlternateWageCode, AlternateWageCodeAdmin)
