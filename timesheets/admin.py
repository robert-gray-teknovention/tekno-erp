from django.contrib import admin
from .models import TimesheetPeriod, TimesheetEntry, UserTimesheetPeriod
# Register your models here.


class TimesheetPeriodAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'date_end', 'org')


class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time_entry', 'date_time_in', 'date_time_out')


class UserTimesheetPeriodAdmin(admin.ModelAdmin):
    list_display = ('user', 'period')


admin.site.register(TimesheetPeriod, TimesheetPeriodAdmin)
admin.site.register(TimesheetEntry, TimesheetEntryAdmin)
admin.site.register(UserTimesheetPeriod, UserTimesheetPeriodAdmin)
