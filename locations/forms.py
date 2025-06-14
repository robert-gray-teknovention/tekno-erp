from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'))
    class Meta:
        model = Location
        fields =['name', 'parent']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'},)
        }