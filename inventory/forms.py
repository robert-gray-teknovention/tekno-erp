from django import forms
from locations.models import Location
from .models import InventoryMaterial, InventoryPart
class InventoryItemMixin():
    def __init__(self, *args, **kwargs):
        self.disabled_fields = kwargs.pop('disabled_fields', None)
        super().__init__(*args, **kwargs)
        if self.disabled_fields:
            for field in self.disabled_fields:
                self.fields[field].widget.attrs['disabled'] = 'disabled'


class InventoryPartForm(InventoryItemMixin, forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = InventoryPart
        fields =['item', 'location', 'quantity']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),

        }
    
    
class InventoryMaterialForm(InventoryItemMixin, forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = InventoryMaterial
        fields =['item', 'location', 'quantity']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

