from django.db import models
from purchasing.models import Part as BasePart
from purchasing.models import Material
from locations.models import Location
from polymorphic.models import PolymorphicModel


class Part(BasePart):
    child_parts = models.ManyToManyField('self', blank=True, through="ChildPart")

    def __str__(self):
        return self.name


class ChildPart(models.Model):
    parent_part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='children')
    child_part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='parents')
    quantity = models.DecimalField(decimal_places=2, max_digits=10, default=1.00)

    class Meta:
        unique_together = ['parent_part', 'child_part']
        constraints = [
            models.CheckConstraint(name='not_same', check=~models.Q(parent_part=models.F('child_part')))
        ]


class InventoryItem(models.Model):
    quantity = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        abstract = True


class InventoryPart(InventoryItem):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    def __str__(self):
        return self.part.name + " " + str(self.quantity)


class InventoryMaterial(InventoryItem):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    def __str__(self):
        return self.material.name + " " + str(self.quantity)


class SerialPart(PolymorphicModel):
    class SerialPartType(models.TextChoices):
        STANDARD = 'STANDARD', 'Standard'
        ASSEMBLY = 'ASSEMBLY', 'Assembly'
        EQUIPMENT = 'EQUIPMENT' 'Equipment'
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    parent_serial_part = models.ForeignKey('self', on_delete=models.CASCADE, related_name='serial_children',
                                           null=True, blank=True)
    serial_description = models.CharField(max_length=255, null=True, blank=True)
    man_serial_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    type = models.CharField(max_length=20, choices=SerialPartType.choices, default=SerialPartType.STANDARD)
    name = part.name

    def __str__(self):
        return self.part.name


class Equipment(SerialPart):
    equipment_info = models.JSONField(null=True, default=dict)

    def __str__(self):
        return self.part.name

    
