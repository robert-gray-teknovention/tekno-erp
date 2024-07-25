from django.db import models
from timesheets.models import TimesheetEntry
from projects.models import Project
from inventory.models import Equipment
from datetime import datetime


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
        MISC = 'MISC', 'Miscellaneous'
    accrue_date = models.DateField(default=datetime.now())
    total_cost = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    type = models.CharField(max_length=20, choices=ExpenseType.choices, default=ExpenseType.MISC)


class Mileage(Expense):
    miles = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE)
    entry = models.ForeignKey(TimesheetEntry, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.miles * self.rate.value
        self.type = Expense.ExpenseType.MILEAGE
        if self.entry:
            self.project = self.entry.project
        super().save(*args, **kwargs)
