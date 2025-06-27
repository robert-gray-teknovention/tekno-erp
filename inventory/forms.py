from django import forms
from locations.models import Location
from .models import InventoryMaterial, InventoryPart

class InventoryPartForm(forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = InventoryPart
        fields =['item', 'location', 'quantity']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),

        }

class InventoryMaterialForm(forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = InventoryMaterial
        fields =['item', 'location', 'quantity']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

