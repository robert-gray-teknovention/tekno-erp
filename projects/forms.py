from django import forms
from .models import Project, ProjectDocumentation as Documentation
from django_select2 import forms as s2forms
from searchableselect.widgets import SearchableSelect
from django.core.exceptions import ValidationError
from datetime import datetime
from django.conf import settings
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
            # 'organizations': forms.HiddenInput(),
        }


class ProjectDocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ['file']
