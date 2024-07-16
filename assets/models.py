from django.db import models
from inventory.models import Equipment


class Asset(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    equipment = models.OneToOneField(Equipment, null=True, on_delete=models.SET_NULL)
    date_acquired = models.DateTimeField()
    date_retired = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.equipment is not None:
            self.name = self.equipment.part.name
        super(Asset, self).save(*args, **kwargs)


class Vehicle(Asset):
    total_mileage = models.DecimalField(decimal_places=1, max_digits=10)


class Building(Asset):
    year_built = models.IntegerField(max_length=4)
