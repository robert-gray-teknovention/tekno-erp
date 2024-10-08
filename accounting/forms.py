from django.forms import ModelForm, HiddenInput, Select, BooleanField, ModelChoiceField
from django_select2 import forms as s2forms
from .models import Expense, Mileage, Lodging, Transportation, Meals, Misc, Service
# from .models import Expense, Mileage
from purchasing.models import Vendor, PaymentAccount
from . import forms
'''class ExpenseSearchWidget(s2forms.ModelSelect2Widget):
    model = Expense
    search_fields = [
        "name__icontains",
    ]
'''


class ExpenseForm(ModelForm):
    delete = BooleanField(label='Delete Expense', required=False)

    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'project': Select(attrs={'class': 'form-control'}),
            'equipment': Select(attrs={'class': 'form-control'}),
            'entry': Select(attrs={'class': 'form-control'}),
            # 'entry': HiddenInput(),
            'user': HiddenInput(),
            'type': HiddenInput(),

        }


class VendorExpenseForm(ExpenseForm):
    payment = ModelChoiceField(queryset=PaymentAccount.objects.filter(active=True), widget=Select(attrs={'class': 'form-control'}), blank=True, required=False)


class MileageForm(ExpenseForm):
    class Meta:
        model = Mileage
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        widgets['rate'] = Select(attrs={'class': 'form-control'})


class LodgingForm(VendorExpenseForm):
    class Meta:
        model = Lodging
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        # widgets['vendor'] = Select(attrs={'class': 'form-control'})
    vendor = ModelChoiceField(queryset=Vendor.objects.filter(type__name__icontains='lodging').order_by('name'),
                              widget=Select(attrs={'class': 'form-control'}))


class TransportationForm(VendorExpenseForm):
    class Meta:
        model = Transportation
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        widgets['vendor'] = Select(attrs={'class': 'form-control'})
        widgets['transportation_type'] = Select(attrs={'class': 'form-control'})

    vendor = ModelChoiceField(queryset=Vendor.objects.filter(type__name__icontains='transportation').order_by('name'),
                              widget=Select(attrs={'class': 'form-control'}))


class MealsForm(VendorExpenseForm):
    class Meta:
        model = Meals
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        widgets['meal_type'] = Select(attrs={'class': 'form-control'})
    vendor = ModelChoiceField(queryset=Vendor.objects.filter(type__name__in=list(zip(*Meals.MealType.choices))[1]).order_by('name'), widget=Select(attrs={'class': 'form-control'}))


class ServiceForm(VendorExpenseForm):
    class Meta:
        model = Service
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        labels = {'serv': 'Service'}
        widgets['serv'] = Select(attrs={'class': 'form-control'})
    vendor = ModelChoiceField(queryset=Vendor.objects.filter(type__name__icontains='service').order_by('name'),
                              widget=Select(attrs={'class': 'form-control'}))


class MiscForm(VendorExpenseForm):
    class Meta:
        model = Misc
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        vendor = ModelChoiceField(queryset=Vendor.objects.all().order_by('name'), widget=Select(attrs={'class': 'form-control'}))


def get_expense_form(model_name, *args, **kwargs):
    # print(str(args), ' ', str(kwargs))
    form = getattr(forms, model_name + 'Form')
    if 'instance' in kwargs:
        return form(*args, instance=kwargs['instance'])
    if 'initial' in kwargs:
        return form(*args, initial=kwargs['initial'])
    return form(*args)
