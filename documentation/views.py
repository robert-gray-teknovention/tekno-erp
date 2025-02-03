from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView, TemplateView
from django.forms import modelformset_factory
from .forms import ClassContainingDocumentsForm
from django.utils.module_loading import import_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.


class DocumentationListView(ListView):
    pass


class ClassContaininghDocumentsView(FormView):
    form_class = ClassContainingDocumentsForm
    template_name = 'documentation/doclist.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'documentation/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes_form'] = ClassContainingDocumentsForm()
        return context


class DocumentationCreateView(LoginRequiredMixin, CreateView):
    # fields = ['parent', 'file', 'description']
    template_name = 'documentation/base_doc_form.html'

    def get_model(self):
        model = get_class_case_insensitive('documentation.models', self.kwargs.get('model') + 'Documentation')
        self.model = model
        return model

    def get_form_class(self):
        return get_class_case_insensitive('documentation.forms', self.kwargs.get('model') + 'DocumentationForm')

    def get_existing(self, par_id):
        return self.get_model().objects.filter(parent_id=par_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'parent_id' in self.kwargs:
            context['existing_files'] = self.get_existing(self.kwargs['parent_id'])
        context['formset'] = self.get_formset_blank()
        context['model'] = self.kwargs.get('model')
        return context

    def get_formset_blank(self, parent_id=None):
        formset_initial = []
        if 'parent_id' in self.kwargs:
            formset_initial = [{'parent'.strip(): self.kwargs['parent_id']}]
        if parent_id:
            formset_initial = [{'parent'.strip(): parent_id}]
        return modelformset_factory(
            self.get_model(),
            form=self.get_form_class(),
            can_delete=True,
            extra=1,
        )(queryset=self.get_model().objects.none(), initial=formset_initial)

    def post(self, request, *args, **kwargs):
        formset = modelformset_factory(
            self.get_model(),
            form=self.get_form_class(),
            can_delete=True,
            extra=1,
        )(request.POST, request.FILES)
        if formset.is_valid():
            parent_id = formset.forms[0].cleaned_data['parent'].id
            formset.save()
            return render(
                self.request,
                'documentation/doc_form.html',
                {
                    'formset': self.get_formset_blank(parent_id),
                    'existing_files': self.get_existing(parent_id),
                    'model': self.kwargs['model']},
            )
        return render(
            request,
            'documentation/doc_form.html',
            {'formset': formset, 'existing_files': self.get_existing(parent_id)}
            )


def get_class_case_insensitive(module_path, class_name):
    module = import_string(module_path)
    for name, obj in vars(module).items():
        if name.lower() == class_name.lower() and isinstance(obj, type):
            return obj
    raise ImportError(f"Class '{class_name}' not found in module '{module_path}'")


@login_required
def delete_doc(request, **kwargs):
    if 'model' in kwargs:
        model = get_class_case_insensitive('documentation.forms', kwargs['model'] + 'Documentation')
        if 'id' in kwargs:
            model.objects.filter(id=kwargs['id']).delete()
            return JsonResponse({'status': 'success', 'id': kwargs['id']})
