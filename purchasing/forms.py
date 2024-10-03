from django.forms import ModelForm, HiddenInput, Select, ModelChoiceField
from .models import Vendor, Manufacturer, PurchaseItem, PurchaseOrder, PurchaseOrderItem, Item
from django_select2 import forms as s2forms
from searchableselect.widgets import SearchableSelect


class VendorSearchWidget(s2forms.ModelSelect2Widget):
    model = Vendor
    search_fields = [
        "name__icontains",
    ]


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'website', 'phone', 'notes', 'is_active', 'organization']
        widgets = {
            'organization': HiddenInput(),
        }


'''
class ManufacturerForm(ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'email', 'website', 'phone', 'is_active', 'organization']
        widgets = {
            'organization': HiddenInput(),
        }
'''


def get_company_form(mymodel, *args, **kwargs):

    class CompanyForm(ModelForm):
        class Meta:
            model = mymodel
            # fields = ['name', 'email', 'website', 'phone', 'notes', 'is_active', 'organization']
            exclude = []
            widgets = {
                'organization': HiddenInput(),
            }
        # delete_check = ModelForm.

        def __init__(self):
            super(CompanyForm, self).__init__(*args, **kwargs)
    return CompanyForm()


def get_item_form(mymodel, *args, **kwargs):
    class ItemForm(ModelForm):
        class Meta:
            model = mymodel
            exclude = []
            widgets = {
                'organization': HiddenInput(),
            }

        def __init__(self):
            super(ItemForm, self).__init__(*args, **kwargs)

    return ItemForm()


class PurchaseOrderForm(ModelForm):
    vendor = ModelChoiceField(queryset=Vendor.objects.filter(is_active=True).order_by('name'), widget=Select(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = PurchaseOrder
        exclude = []
        widgets = {
            'organization': HiddenInput(),
            'purchaser': HiddenInput(),
            'orderer': HiddenInput(),
            'status_change_date': HiddenInput(),
            'status': Select(attrs={'class': 'form-control'}),

        }


class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        exclude = []
        fields = ['item', 'vendor', 'manufacturer', 'type']
        widgets = {
            'vendor': HiddenInput(),
            'manufacturer': HiddenInput(),
        }


class PurchaseOrderItemForm(ModelForm):
    class Meta:
        model = PurchaseOrderItem
        exclude = []
        widgets = {
            'purchase_order': HiddenInput(),
            'status_change_date': HiddenInput()
        }

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = '/purchaseorderitem/create/'''
