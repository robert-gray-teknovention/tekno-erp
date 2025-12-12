from django.contrib import admin
from .models import Part, SerialPart, Equipment, InventoryPart, InventoryMaterial


class ChildPartsInline(admin.TabularInline):
    model = Part.child_parts.through
    fk_name = 'parent_part'


class SerialChildPartsInline(admin.TabularInline):
    model = SerialPart

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    inlines = [ChildPartsInline,]


@admin.register(InventoryPart)
class InventoryPartAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'location']

@admin.register(InventoryMaterial)
class InventoryMaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'location']

@admin.register(SerialPart)
class SerialPartAdmin(admin.ModelAdmin):
    list_display = ['id', 'part']
    inlines = (SerialChildPartsInline,)


@admin.register(Equipment)
class Equipment(admin.ModelAdmin):
    list_display = ['id', 'part']
