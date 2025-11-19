from django.urls import path
from .views import (
    WorkOrderCreateView,
    WorkOrderUpdateView,
    WorkOrderDeleteView,
    WorkOrderListView,
    WorkEntryCreateView,
    WorkEntryUpdateView,
    WorkEntryDeleteView,
    WorkEntryListView,
)

app_name = 'workorders'

urlpatterns = [
    # WorkOrder URLs (mounted at /workorders/ via mainapp.urls)
    path('', WorkOrderListView.as_view(), name='workorder-list'),
    path('add/', WorkOrderCreateView.as_view(), name='workorder-add'),
    path('<int:pk>/edit/', WorkOrderUpdateView.as_view(), name='workorder-edit'),
    path('<int:pk>/delete/', WorkOrderDeleteView.as_view(), name='workorder-delete'),

    # WorkEntry URLs mounted under the workorders prefix
    path('workentries/', WorkEntryListView.as_view(), name='workentry-list'),
    path('workentries/add/', WorkEntryCreateView.as_view(), name='workentry-add'),
    path('workentries/<int:pk>/edit/', WorkEntryUpdateView.as_view(), name='workentry-edit'),
    path('workentries/<int:pk>/delete/', WorkEntryDeleteView.as_view(), name='workentry-delete'),
]
