from django.forms import ModelForm, HiddenInput
from .models import Vendor, Manufacturer, PurchaseItem
from django_select2 import forms as s2forms
from searchableselect.widgets import SearchableSelect


class VendorSearchWidget(s2forms.ModelSelect2Widget):
    model = Vendor
    search_fields = [
        "name__icontains",
    ]


'''class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'website', 'phone', 'notes', 'is_active', 'organization']
        widgets = {
            'organization': HiddenInput(),
        }


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
            fields = ['name', 'email', 'website', 'phone', 'notes', 'is_active', 'organization']
            widgets = {
                'organization': HiddenInput(),
            }

        def __init__(self):
            super(CompanyForm, self).__init__(*args, **kwargs)
    return CompanyForm()


"""class PurchaseItemForm(ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['item_name', 'vendor', 'manufacturer', 'type']
"""
