from django.db import models
from organizations.models import Organization
from polymorphic.models import PolymorphicModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Vendor(models.Model):
    class VendorType(models.Model):
        name = models.CharField(max_length=20)

        def __str__(self):
            return self.name
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # organizations = models.ManyToManyField(Organization, through='VendorOrganization')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    notes = models.TextField(null=True)
    type = models.ForeignKey(VendorType, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'organization')


'''class VendorOrganization(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('vendor', 'organization')
    # contacts = models.JSONField(default=dict, null=True)
'''


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Item(PolymorphicModel):
    name = models.CharField(max_length=75, unique=True)
    description = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ': ' + self.organization.name


def default_itemtype_data():
    return []


def default_itemdetails_data():
    return {}


class ItemType(models.Model):
    type_name = models.CharField(max_length=75, unique=True)
    type_description = models.CharField(max_length=255)
    details_list = models.JSONField(default=default_itemtype_data)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PartType(ItemType):
    pass


class Part(Item):
    type = models.ForeignKey(PartType, null=True, on_delete=models.SET_NULL)
    details = models.JSONField(default=default_itemdetails_data)

    def __str__(self):
        return 'Part: '+self.name


class SubscriptionType(ItemType):
    pass


class Subscription(Item):
    is_recurring = models.BooleanField(default=True)
    type = models.ForeignKey(SubscriptionType, null=True, on_delete=models.SET_NULL)
    details = models.JSONField(default=default_itemdetails_data)

    def __str__(self):
        return 'Subscription: '+self.name


class ServiceType(ItemType):
    pass


class Service(Item):
    is_recurring = models.BooleanField(default=False)
    type = models.ForeignKey(ServiceType, null=True, on_delete=models.SET_NULL)
    details = models.JSONField(default=default_itemdetails_data)

    def __str__(self):
        return 'Service: ' + self.name


class MaterialType(ItemType):
    pass


class Material(Item):
    type = models.ForeignKey(MaterialType, null=True, on_delete=models.SET_NULL)
    details = models.JSONField(default=default_itemdetails_data)

    def __str__(self):
        return 'Material ' + self.name


class PaymentAccount(models.Model):
    class AccountType(models.TextChoices):
        SAVINGS = 'SAVINGS', 'Savings'
        CHECKING = 'CHECKING', 'Checking'
        CREDIT = 'CREDIT', 'Credit'
        CASH = 'CASH', 'Cash'

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=AccountType.choices, default=AccountType.CASH)
    last_four = models.CharField(null=True, max_length=4, blank=True)
    active = models.BooleanField(default=True)
    '''Implement in the future expiration, expired, account number after implementing encryption on these fields'''

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = 'CREATED', 'Created'
        SUBMITTED = 'SUBMITTED', 'Submitted for Approval'
        APPROVED = 'APPROVED', 'Approved for Ordering'
        ORDERED = 'ORDERED', 'Ordered'
        CLOSED = 'CLOSED', 'Closed'
        CANCELED = 'CANCELED', 'Canceled'
        IN_PERSON = 'IN_PERSON', 'In Person Purchase'

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    sub_total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    shipping = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    tax = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    status_change_date = models.DateTimeField(auto_now=True)
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchaser_pos', null=True, blank=True)
    orderer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderer_pos', null=True)

    def __str__(self):
        return self.vendor.name + ' ' + str(self.create_date) + ' ' + self.purchaser.first_name + ' ' + self.purchaser.last_name


class Payment(models.Model):
    payment_date = models.DateTimeField()
    account = models.ForeignKey(PaymentAccount, null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.payment_date + ' ' + self.account.name)


class PurchaseItem(models.Model):
    class ItemType(models.TextChoices):
        SUBSCRIPTION = 'SUBS', 'Subscription'
        PART = 'PART', 'Part'
        SERVICE = 'SERV', 'Service'
        MATERIAL = 'MATERIAL', 'Material'

    class Units(models.TextChoices):
        EACH = 'EACH', 'Each'
        HOUR = 'HOUR', 'Hourly'
        PACK = 'PACK', 'Pack'
        WEEK = 'WEEK', 'Weekly'
        MONTH = 'MONTH', 'Monthly'
        YEAR = 'YEAR', 'Yearly'

    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    vendor = models.ManyToManyField(Vendor)
    manufacturer = models.ManyToManyField(Manufacturer)
    type = models.CharField(max_length=25, default=ItemType.PART, choices=ItemType.choices)
    units = models.CharField(max_length=10, default=Units.EACH, choices=Units.choices)

    def __str__(self):
        return self.item.name

    class Meta:
        unique_together = ('item', 'units')


class PurchaseOrderItem(models.Model):
    class ItemStatus(models.TextChoices):
        ENTERED = "ENTERED", 'Entered'
        ORDERED = 'ORDERED', 'Ordered'
        RECEIVED = 'RECEIVED', 'Received'

    purchase_item = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=ItemStatus.choices, default=ItemStatus.ENTERED)
    status_change_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purchase_item.item.name

    class Meta:
        unique_together = ('purchase_order', 'purchase_item')


class PurchaseOrderItemHistory(models.Model):
    purchase_order_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default=PurchaseOrderItem.ItemStatus.ENTERED)
    status_change_date = models.DateTimeField(auto_now=True)


class PurchaseOrderHistory(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default=PurchaseOrder.OrderStatus.CREATED)
    status_change_date = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=PurchaseOrderItem)
def purchase_order_item_history_add(sender, **kwargs):
    create = True
    poi = kwargs.get('instance')
    if not kwargs.get('created'):
        history = PurchaseOrderItemHistory.objects.filter(purchase_order_item=poi).last()
        if history.status == poi.status:
            create = False
    if create:
        history = PurchaseOrderItemHistory()
        history.status = poi.status
        history.purchase_order_item = poi
        history.save()


@receiver(post_save, sender=PurchaseOrder)
def purchase_order_history_add(sender, **kwargs):
    create = True
    po = kwargs.get('instance')
    if not kwargs.get('created'):
        history = PurchaseOrderHistory.objects.filter(purchase_order=po).last()
        if history.status == po.status:
            create = False
    if create:
        history = PurchaseOrderHistory()
        history.status = po.status
        history.purchase_order = po
        history.save()
