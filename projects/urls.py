from django.urls import path
from django.views.generic import ListView
from .models import Project
from . import views
# from .views import VendorListView

urlpatterns = [
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/', ListView.as_view(model=Project, template_name="projects/projectlist.html"), name='project_list'),
    path('delete-documentation/', views.delete_project_documentation, name='delete_project_documentation'),
    ]
