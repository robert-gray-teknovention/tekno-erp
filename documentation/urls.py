from django.urls import path
from django.views.generic import ListView
from .models import Documentation
from . import views
# from .views import VendorListView

urlpatterns = [
    path('doc/create/<str:model>/', views.DocumentationCreateView.as_view(), name='doc_create'),
    # path('documentation/<int:pk>/update/', views.DocumentationUpdateView.as_view(), name='doc_update'),
    path(
        'docs/',
        ListView.as_view(model=Documentation, template_name="documentation/doclist.html"), name='doclist'
        ),
    path('dashboard/', views.DashboardView.as_view(), name='doc_dashboard'),
    ]
