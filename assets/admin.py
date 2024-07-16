from django.contrib import admin
from .models import Asset, Vehicle, Building
# Register your models here.


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
