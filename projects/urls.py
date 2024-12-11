from django.urls import path
from django.views.generic import ListView
from .models import Project
from . import views
# from .views import VendorListView

urlpatterns = [
    path('project/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/', ListView.as_view(model=Project, template_name="projects/Proje"), name='project_list'),

    ]
