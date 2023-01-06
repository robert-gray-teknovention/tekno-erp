from django.contrib import admin
from .models import Approval


'''class ApprovalInLine(admin.TabularInline):
    model = .approvees.through
    extra = 1
    fk_name = "from_timesheetuser"
'''


'''class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('approver', 'approvee', 'timesheet_entry')
'''


admin.site.register(Approval)
