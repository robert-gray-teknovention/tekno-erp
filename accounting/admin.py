from django.contrib import admin
from .models import Rate, Mileage, Expense


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass


@admin.register(Mileage)
class MileageAdmin(admin.ModelAdmin):
    list_display = ('accrue_date', 'equipment')


@admin.register(Expense)
class ExpensAdmin(admin.ModelAdmin):
    pass
