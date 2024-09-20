from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from .models import Vendor, Manufacturer, Item, PurchaseItem
from .models import PurchaseOrderItem, PurchaseOrder, PurchaseOrderItemHistory, PurchaseOrderHistory
from .models import Part, Service, Subscription
from .models import PaymentAccount, Payment


# class OrganizationsInline(admin.TabularInline):
#    model = Vendor.organizations.through


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'phone', 'type', 'is_active')
    # inlines = [OrganizationsInline,]

    @admin.register(Vendor.VendorType)
    class VendorTypeAdmin(admin.ModelAdmin):
        pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'website', 'phone', 'is_active', 'notes')


class ItemChildAdmin(PolymorphicChildModelAdmin):
    base_model = Item  # Optional, explicitly set here.

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    base_fieldsets = (
        ("Base Item", {
          'fields': ('name', 'description')
          }),
    )


@admin.register(PaymentAccount)
class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'active')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_date', 'amount')


@admin.register(Part)
class PartAdmin(ItemChildAdmin):
    pass


@admin.register(Subscription)
class SubscriptionAdmin(ItemChildAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(ItemChildAdmin):
    list_display = ('name', 'description')


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    pass


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_item']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'vendor', 'create_date', 'status']


@admin.register(PurchaseOrderItemHistory)
class PurchaseOrderItemHistory(admin.ModelAdmin):
    list_display = ['purchase_order_item', 'status', 'status_change_date']


@admin.register(PurchaseOrderHistory)
class PurchaseOrderHistory(admin.ModelAdmin):
    list_display = ['purchase_order', 'status', 'status_change_date']


@admin.register(Item)
class ItemParentAdmin(PolymorphicParentModelAdmin):
    base_model = Item  # Optional, explicitly set here.
    child_models = (Part, Subscription, Service)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
