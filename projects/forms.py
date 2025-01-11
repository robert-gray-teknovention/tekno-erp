from django import forms
from .models import Project, ProjectDocumentation as Documentation
from django_select2 import forms as s2forms
from searchableselect.widgets import SearchableSelect
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings
from django.forms import modelformset_factory
import os


class ProjectSearchWidget(s2forms.ModelSelect2Widget):
    model = Project
    search_fields = [
        "name__icontains",
    ]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'contributors': forms.CheckboxSelectMultiple(),
            'organizations': forms.CheckboxSelectMultiple(),
        }


class ProjectDocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ['file', 'description']


ProjectDocumentationFormSet = modelformset_factory(
    Documentation,
    form=ProjectDocumentationForm,
    can_delete=True,
    extra=0)
