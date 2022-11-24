from django.contrib import admin
from .models import Organization, PeriodType
# Register your models here.


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'street1', 'street2', 'city', 'zip', 'state', 'phone', 'email')


class PeriodTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(PeriodType, PeriodTypeAdmin)
