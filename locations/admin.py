from django.contrib import admin
from .models import Location

class ChildLocationInline(admin.TabularInline):
    model = Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name',]
    inlines = [ChildLocationInline]
    