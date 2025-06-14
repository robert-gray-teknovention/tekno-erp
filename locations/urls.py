from django.urls import path
from .views import (
    LocationListView, LocationCreateView,
    LocationUpdateView, LocationDeleteView, LocationDetailView
)

urlpatterns = [
    path('', LocationListView.as_view(), name='location_tree'),
    path('add/', LocationCreateView.as_view(), name='location_add'),
    path('<int:parent_id>/add/', LocationCreateView.as_view(), name='location_add'),
    path('<int:pk>/edit/', LocationUpdateView.as_view(), name='location_edit'),
    path('<int:pk>/delete/', LocationDeleteView.as_view(), name='location_delete'),
    path('<int:pk>/delete/<int:parent_id>', LocationDeleteView.as_view(), name='location_delete'),
    path('<int:pk>/', LocationDetailView.as_view(), name='location_detail'),
]
