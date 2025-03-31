from django.contrib import admin
from .models import ItemDocumentation, TimesheetEntryDocumentation


# Register your models here.
@admin.register(ItemDocumentation)
class ItemDocumentationAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(TimesheetEntryDocumentation)
class TimesheetEntryDocumentationAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
