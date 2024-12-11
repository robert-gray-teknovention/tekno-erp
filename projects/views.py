from django.shortcuts import render
from .models import Project, ProjectDocumentation as Documentation
from .forms import ProjectForm, ProjectDocumentationForm as DocumentationForm
from django.views.generic.edit import CreateView
from django.forms.models import inlineformset_factory
# Create your views here.


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project.html'
    success_url = 'projects/projectlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DocumentationFormSet = inlineformset_factory(Project, Documentation, form=DocumentationForm, extra=3)
        if self.request.POST:
            context['formset'] = DocumentationFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = DocumentationFormSet()
        return context

    def post(self, request, *args, **kwargs):
        print("Files", request.FILES)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("form is valid Yo")
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            print("we are about to save the formset!!")
            formset.save()
            return super().form_valid(form)
        else:
            print("The formset is invalid !!")
            return super().form_invalid(form)

    def form_invalid(self, form):
        print("We have errors ", form.errors)
