from django.contrib import admin
from .models import Organization
# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'street1', 'street2', 'city', 'zip', 'state', 'phone', 'email')


admin.site.register(Organization)
