from django.forms import (
    Form,
    ModelForm,
    HiddenInput,
    Select,
    ModelChoiceField,
    ChoiceField,
    SelectMultiple,
    ModelMultipleChoiceField, CheckboxSelectMultiple, BooleanField, CheckboxInput,
    NumberInput, DateField, DateInput)
from .models import Vendor, Manufacturer, PurchaseItem, PurchaseOrder, PurchaseOrderItem, Item
from projects.models import Project
from django_select2 import forms as s2forms
from searchableselect.widgets import SearchableSelect
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.safestring import mark_safe
import os


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
        # child_parts = MultipleChoiceField(widget=HiddenInput(), required=False, default=[])

        class Meta:
            model = mymodel
            exclude = []
            widgets = {
                'organization': HiddenInput(),
                'type': Select(attrs={'class': 'form-control'}),
                'child_parts': SelectMultiple(attrs={'class': 'form-control'}),
            }

        # def __init__(self):
        #    super(ItemForm, self).__init__(*args, **kwargs)
    return ItemForm


class ItemTypeForm(Form):
    type_choices = (
        ('Part', 'PART'),
        ('Material', 'MATERIAL'),
        ('Service', 'SERVICE'),
        ('Subscription', 'SUBSCRIPTION'),
    )
    item_type = ChoiceField(choices=type_choices)


class PurchaseOrderForm(ModelForm):
    vendor = ModelChoiceField(queryset=Vendor.objects.filter(is_active=True).order_by('name'), widget=Select(attrs={'class': 'form-control'}), required=True)
    project = ModelChoiceField(queryset=Project.objects.filter(active=True, ).order_by('name'), widget=Select(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = PurchaseOrder
        exclude = []
        widgets = {
            'organization': HiddenInput(),
            'purchaser': HiddenInput(),
            'orderer': HiddenInput(),
            'status_change_date': HiddenInput(),
            'status': Select(attrs={'class': 'form-control'}),
            'purchase_date': DateInput(attrs={'type': 'date'}),
            'project': Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'organization' in self.initial:
            org = self.initial['organization']
            self.fields['project'].queryset = Project.objects.filter(active=True, organizations__in=[org]).order_by('name')

    def clean_invoice(self):
        uploaded_file = self.cleaned_data.get('invoice')
        if uploaded_file:
            # Check file size (in bytes)
            max_size = 6 * 1024 * 1024  # 2 MB
            if uploaded_file.size > max_size:
                print("Error File is too big ")
                raise ValidationError("File size must be less than " + str(max_size) + " MB.")
            # Rename file
            original_name, ext = os.path.splitext(uploaded_file.name)
            new_name = f"po-inv-{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"  # Customize the new name as needed
            uploaded_file.name = new_name
            print("We are going to upload the file! " + uploaded_file.name)
        return uploaded_file


class PurchaseItemForm(ModelForm):
    manufacturer = ModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        widget=CheckboxSelectMultiple,
        # widget=HiddenInput()
        )

    class Meta:
        model = PurchaseItem
        exclude = []
        # fields = ['item', 'vendor', 'manufacturer', 'type']
        widgets = {
            # 'vendor': HiddenInput(),
            # 'manufacturer': HiddenInput(),
            'item': Select(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            # 'type': HiddenInput(),
        }


class PurchaseOrderItemForm(ModelForm):
    delete = BooleanField(label='Remove', required=False, disabled=True, widget=CheckboxInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PurchaseOrderItem
        exclude = []
        widgets = {

            'purchase_item': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            # 'unit_cost': MoneyWidget(amount_widget=NumberInput(attrs={'class': 'form-control'}))
        }


    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = '/purchaseorderitem/create/'''
