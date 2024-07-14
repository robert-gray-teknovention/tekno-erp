from django.db import models


class Rate(models.Model):
    name = models.TextField()


class Expense(models.Model):
    total_cost = models.DecimalField(decimal_places=2, max_digits=10)


class Mileage(Expense):
    accrue_date = models.DateField(auto_now=True)
    miles = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    rate = models.ForeignKey(Rate, on_delete=models.SET_NULL)
