from django.contrib import admin
from .models import TimesheetPeriod, TimesheetEntry
# Register your models here.


class TimesheetPeriodAdmin(admin.ModelAdmin):
    list_display = ('date_start', 'date_end', 'org')


class TimesheetEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time_entry', 'date_time_in', 'date_time_out')


admin.site.register(TimesheetPeriod, TimesheetPeriodAdmin)
admin.site.register(TimesheetEntry, TimesheetEntryAdmin)
