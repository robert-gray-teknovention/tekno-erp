from django.contrib import admin
from .models import Organization, PeriodType
# Register your models here.


class ManagersInLine(admin.TabularInline):
    model = Organization.managers.through
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'street1', 'street2', 'city', 'zip', 'state', 'phone', 'mailer_email')
    inlines = [
        ManagersInLine,
    ]


class PeriodTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PeriodType, PeriodTypeAdmin)
