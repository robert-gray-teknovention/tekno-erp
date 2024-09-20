from django.db import models
from timesheets.models import TimesheetEntry, TimesheetUser
from projects.models import Project
from inventory.models import Equipment
from datetime import datetime
from purchasing.models import Vendor, Service, PaymentAccount


class Rate(models.Model):
    name = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Expense(models.Model):
    class ExpenseType(models.TextChoices):
        MILEAGE = 'MILEAGE', 'Mileage'
        MEALS = 'MEALS', 'Meals'
        TRANSPORTATION = 'TRANSPORTATION', 'Transportation'
        LODGING = 'LODGING', 'Lodging'
        SERVICE = 'SERVICE', 'Service'
        MISC = 'MISC', 'Misc'
    accrue_date = models.DateField(default=datetime.now())
    type = models.CharField(max_length=20, choices=ExpenseType.choices, default=ExpenseType.MISC)
    user = models.ForeignKey(TimesheetUser, on_delete=models.CASCADE, null=True, blank=True)
    entry = models.ForeignKey(TimesheetEntry, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    total_cost = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class VendorExpense(Expense):
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    receipt = models.URLField(null=True, blank=True)
    payment = models.ForeignKey(PaymentAccount, null=True, on_delete=models.SET_NULL, blank=True)


class Mileage(Expense):
    miles = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.miles * self.rate.value
        self.type = Expense.ExpenseType.MILEAGE
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)


class Lodging(VendorExpense):
    nightly_rate = models.DecimalField(max_digits=5, decimal_places=2)
    nights = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total_cost = self.nightly_rate * self.nights
        self.type = Expense.ExpenseType.LODGING
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)


class Transportation(Expense):
    class TransportationType(models.TextChoices):
        BUS = 'BUS', 'Bus'
        AIR = 'AIR', 'Airfare'
        TAXI = 'TAXI', 'Taxi'
        RIDE = 'RIDE', 'Rideshare'
        TRAIN = 'TRAIN', 'Train'

    transportation_type = models.CharField(max_length=10, choices=TransportationType.choices, null=True)

    def save(self, *args, **kwargs):
        self.type = Expense.ExpenseType.TRANSPORTATION
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)


class Meals(Expense):
    class MealType(models.TextChoices):
        RESTAURANT = 'RESTAURANT', 'Restaurant'
        GROCERIES = 'GROCERIES', 'Groceries'
    meal_type = models.CharField(max_length=20, choices=MealType.choices, null=True)
    cost = models.DecimalField(decimal_places=2, max_digits=5)
    tip = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)

    def save(self, *args, **kwargs):
        self.total_cost = self.cost + self.tip
        self.type = Expense.ExpenseType.MEALS
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)


class Misc(Expense):

    def save(self, *args, **kwargs):
        self.type = Expense.ExpenseType.MISC
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)


class ServiceExpense(Expense):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.type = Expense.ExpenseType.SERVICE
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)
