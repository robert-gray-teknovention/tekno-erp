from django.db import models
from purchasing.models import Part as BasePart, Item
from purchasing.models import Material, Food
from locations.models import Location
from polymorphic.models import PolymorphicModel
from timesheets.models import TimesheetUser

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
    units = models.CharField(max_length=50, null=True, blank=True, default='each')
    class Meta:
        abstract = True
    
    def get_class_name(self):
        return self.__class__.__name__
    

class InventoryItemUniqueMixin():
    def save(self, *args, **kwargs):
        if self._state.adding:
            existing = self.__class__.objects.filter(location=self.location, item=self.item).first()
            if existing:
                existing.quantity += self.quantity
                self = existing
        super().save(*args, **kwargs)


class InventoryPart(InventoryItemUniqueMixin, InventoryItem):
    item = models.ForeignKey(Part, on_delete=models.CASCADE)
    def __str__(self):
        return self.item.name + " " + str(self.quantity)

    def get_item_type(self):
        return 'part'

    

class InventoryMaterial( InventoryItemUniqueMixin, InventoryItem):
    item = models.ForeignKey(Material, on_delete=models.CASCADE)
    def __str__(self):
        return self.item.name + " " + str(self.quantity)
    
    def get_item_type(self):
        return 'material'

class InventoryFood(InventoryItemUniqueMixin, InventoryItem):
    item = models.ForeignKey(Food, on_delete=models.CASCADE)
    def __str__(self):
        return self.item.name + " " + str(self.quantity)
    
    def get_item_type(self):
        return 'food'

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

    
class InventoryItemTransaction(models.Model):
    class TransactionType(models.TextChoices):
        CREATE = 'CREATE', 'Create'
        UPDATE = 'UPDATE', 'Update'
        DELETE = 'DELETE', 'Delete'
        ADDITION = 'ADDITION', 'Addition'
        SUBTRACTION = 'SUBTRACTION', 'Subtraction'
        TRASH = 'REMOVAL', 'Removal'
        USAGE = 'USAGE', 'Usage'
        SOURCE_TRANSFER = 'SOURCE_TRANSFER', 'Source Transfer'
        DESTINATION_TRANSFER = 'DESTINATION_TRANSFER', 'Destination Transfer'
    inventory_item_id = models.IntegerField(default=0, null=True)
    transfer_transaction_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    units = models.CharField(max_length=50, null=True, blank=True, default='each')
    timestamp = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(TimesheetUser, on_delete=models.SET_NULL, null=True, blank=True)
    # notes = models.TextField(null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)

    def __str__(self):
        return f"Transaction for {self.inventory_item_id} on {self.timestamp}"
    
    @property
    def notes(self):
        if self.transaction_type == self.TransactionType.DELETE:
            return f"{self.transaction_type} {self.quantity} {self.units} of {self.item.name} from {self.location.name} on {self.timestamp} by {self.performed_by}"
        else:
            return f"{self.transaction_type} {self.quantity} {self.units} of {self.item.name} at {self.location.name} on {self.timestamp} by {self.performed_by}"
        # return f"{self.transaction_type} {self.quantity} {self.units} of {self.item.name} at {self.location.name} on {self.timestamp} by {self.performed_by}"
    
    