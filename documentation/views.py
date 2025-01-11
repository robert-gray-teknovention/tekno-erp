from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView, TemplateView
from . import models
from . import forms
from django.forms import modelformset_factory
from .forms import ClassContainingDocumentsForm
import importlib
from django.utils.module_loading import import_string
from extra_views import ModelFormSetView
from django.shortcuts import render
# Create your views here.


class DocumentationListView(ListView):
    pass


class ClassContaininghDocumentsView(FormView):
    form_class = ClassContainingDocumentsForm
    template_name = 'documentation/doclist.html'


class DashboardView(TemplateView):
    template_name = 'documentation/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes_form'] = ClassContainingDocumentsForm()
        return context


class DocumentationCreateView(CreateView):
    # fields = ['parent', 'file', 'description']
    template_name = 'documentation/doc_form.html'

    def get_model(self):
        model = get_class_case_insensitive('documentation.models', self.kwargs.get('model') + 'Documentation')
        # print("model ", str(model))
        # self.model = model
        return model

    def get_form_class(self):
        '''formset = formset_factory(get_class_case_insensitive(
            'documentation.forms', self.kwargs.get('model') + 'DocumentationForm')
            )'''
        # self.form_class = formset
        # return formset
        # return self.form_class
        # return getattr(forms, self.kwargs.get('model').capitalize() + 'DocumentationForm')
        return get_class_case_insensitive('documentation.forms', self.kwargs.get('model') + 'DocumentationForm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = modelformset_factory(
            self.get_model(),
            form=self.get_form_class(),
            can_delete=True,
            extra=1,
        )(queryset=self.get_model().objects.none())
        return context
        '''if self.request.method == 'POST':
            context['formset'] = forms.ItemDocumentationFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=self.get_model().objects.none()
                )
        else:
            # context['formset'] = self.form_class()
            context['formset'] = forms.ItemDocumentationFormSet(
                queryset=self.get_model().objects.none()
            )

        return context'''

    def post(self, request, *args, **kwargs):
        formset = modelformset_factory(
            self.get_model(),
            form=self.get_form_class(),
            can_delete=True,
            extra=1,
        )(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
        else:
            print("Formset is invalid")
        return render(request, self.template_name, {'formset': formset})


def get_class_case_insensitive(module_path, class_name):
    module = import_string(module_path)
    for name, obj in vars(module).items():
        if name.lower() == class_name.lower() and isinstance(obj, type):
            return obj
    raise ImportError(f"Class '{class_name}' not found in module '{module_path}'")
