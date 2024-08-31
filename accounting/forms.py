from django.forms import ModelForm, HiddenInput, Select
from django_select2 import forms as s2forms
from .models import Expense, Mileage, Lodging
from . import forms
'''class ExpenseSearchWidget(s2forms.ModelSelect2Widget):
    model = Expense
    search_fields = [
        "name__icontains",
    ]
'''


class ExpenseForm(ModelForm):
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


class MileageForm(ExpenseForm):
    class Meta:
        model = Mileage
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets
        widgets['rate'] = Select(attrs={'class': 'form-control'})


class LodgingForm(ExpenseForm):
    class Meta:
        model = Lodging
        fields = ExpenseForm.Meta.fields
        widgets = ExpenseForm.Meta.widgets


def get_expense_form(model_name, *args, **kwargs):
    # print(str(args), ' ', str(kwargs))
    form = getattr(forms, model_name + 'Form')
    if 'instance' in kwargs:
        return form(*args, instance=kwargs['instance'])
    if 'initial' in kwargs:
        return form(*args, initial=kwargs['initial'])
    return form(*args)
