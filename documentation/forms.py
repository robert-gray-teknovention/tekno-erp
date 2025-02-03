from django import forms
from .models import ItemDocumentation, TimesheetEntryDocumentation
from django.apps import apps
import inspect


class ClassContainingDocumentsForm(forms.Form):
    CLASSES = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        installed_apps = apps.get_app_configs()
        for app_config in installed_apps:
            if app_config.models_module:
                for name, member in inspect.getmembers(app_config.models_module):
                    if inspect.isclass(member):
                        if hasattr(member, 'docs') and app_config.name + '.models' == member.__module__:
                            self.CLASSES = self.CLASSES + ((member.__module__ + '.' + member.__name__, app_config.name
                                                            + ' ' + member.__name__),)
        self.fields['classes'] = forms.ChoiceField(
            choices=self.CLASSES,
            widget=forms.Select(attrs={'class': 'form-control'}),
            required=True)


class DocFormInitMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].empty_label = None
        if 'parent' in self.initial:
            model = self.Meta.model._meta.get_field('parent').related_model
            self.fields['parent'].queryset = model.objects.filter(id=self.initial['parent'])


class ItemDocumentationForm(DocFormInitMixin, forms.ModelForm):
    class Meta:
        model = ItemDocumentation
        fields = ['parent', 'file', 'description']


class TimesheetEntryDocumentationForm(DocFormInitMixin, forms.ModelForm):
    class Meta:
        model = TimesheetEntryDocumentation
        fields = ['parent', 'file', 'description']
