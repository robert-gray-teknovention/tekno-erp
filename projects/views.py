from .models import Project, ProjectDocumentation
from django_tables2.views import SingleTableView
from .forms import ProjectForm, ProjectDocumentationFormSet
from .tables import ProjectTable
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
# Create your views here.


class ProjectListView(LoginRequiredMixin, SingleTableView):
    table_class = ProjectTable
    model = Project
    # filterset_class = ProjectFilter
    template_name = 'projects/projectlist.html'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project.html'
    success_url = 'projects/projectlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProjectDocumentationFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=ProjectDocumentation.objects.none()
                )
        else:
            context['formset'] = ProjectDocumentationFormSet(
                queryset=ProjectDocumentation.objects.none()
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            # formset.instance = self.object
            for doc_form in formset:
                if doc_form.cleaned_data.get('file'):
                    ProjectDocumentation.objects.create(project=self.object, file=doc_form.cleaned_data['file'])
            return super().form_valid(form)
        else:
            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('project_list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['existing_files'] = ProjectDocumentation.objects.filter(project=self.object)
        if self.request.POST:
            print("Here are the files ", self.request.FILES)
            context['formset'] = ProjectDocumentationFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=ProjectDocumentation.objects.filter(project=self.object)
            )
        else:
            context['formset'] = ProjectDocumentationFormSet(
                # initial=[{'file': doc.file} for doc in self.object.documentation.all()]
                # queryset=ProjectDocumentation.objects.filter(project=self.object)
                queryset=ProjectDocumentation.objects.none()
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            # Clear old documentation
            # self.object.documentation.all().delete()
            # Add new documentation

            for doc_form in formset:
                if doc_form.cleaned_data.get('file'):
                    uploaded_file = doc_form.cleaned_data['file']
                    if not ProjectDocumentation.objects.filter(project=self.object, file=uploaded_file.name).exists():
                        ProjectDocumentation.objects.create(
                            project=self.object,
                            file=uploaded_file,
                            description=doc_form.cleaned_data.get('description')
                        )

            return super().form_valid(form)
        else:
            print("Form errors", form.errors())
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('project_list')  # Replace with your success URL


@login_required
def delete_project_documentation(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')
        if doc_id:
            documentation = get_object_or_404(ProjectDocumentation, id=doc_id)
            documentation.delete()
            return JsonResponse({'message': 'File deleted successfully'})
        return JsonResponse({'error': 'File ID not provided'})
    return JsonResponse({'error': 'Invalid request method'})
