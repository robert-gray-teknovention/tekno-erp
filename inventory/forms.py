from django import forms
from locations.models import Location
from .models import InventoryMaterial, InventoryPart, Part, InventoryFood
from purchasing.models import Material, Food
class InventoryItemMixin():
    item_id = None
    def __init__(self, *args, **kwargs):
        self.disabled_fields = kwargs.pop('disabled_fields', None)
        super().__init__(*args, **kwargs)
        if self.disabled_fields:
            for field in self.disabled_fields:
                self.fields[field].widget.attrs['disabled'] = 'disabled'
                
        # For bound forms (submitted data)
        if self.data.get('item'):
            self.item_id = self.data.get('item')
            
        # For existing     
        elif self.instance and self.instance.pk:
            self.item_id = self.instance.item_id

        

class InventoryPartForm(InventoryItemMixin, forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = InventoryPart
        fields =['item', 'location', 'quantity', 'units']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }
    
    
class InventoryMaterialForm(InventoryItemMixin, forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = InventoryMaterial
        fields =['item', 'location', 'quantity', 'units']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }


class InventoryFoodForm(InventoryItemMixin, forms.ModelForm):
    class Meta:
        model = InventoryFood
        fields =['item', 'location', 'quantity', 'units']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

