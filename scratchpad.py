import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainapp.settings')
django.setup()
from locations.models import Location
from inventory.models import Part, InventoryPart
from organizations.models import Organization



org = Organization.objects.get(name__icontains="teknovention")
parts = Part.objects.filter(name__icontains="resistor", organization=org)
i=1
print(org.name)
for part in parts:
    print(part.name)
    loca_val = part.name.split(' Ohm')[0]
    print(loca_val)
    location, created = Location.objects.get_or_create(
        name="Resistor Can " + loca_val,
        defaults={
            "description": "Resistor storage location " + loca_val,
        },
    )
    inventory_item, created = InventoryPart.objects.get_or_create(
        item=part,
        quantity=4,
        location=location,
    )
    print("Created inventory item for part ", part.name, " at location ", location.name)
    