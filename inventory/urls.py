from django.urls import path
from .views import (
    InventoryItemListView, InventoryItemCreateView,
    InventoryItemUpdateView, InventoryItemDeleteView
)

urlpatterns = [
    path('<str:model_name>/', InventoryItemListView.as_view(), name='inventory_list'),
    path('add/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('add/<str:model_name>/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('add/<str:model_name>/<int:initial_id>/<success_url>', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('add/<str:model_name>/<str:initial_type>/<int:initial_id>/<str:success_url>/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('edit/', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('edit/<int:pk>', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('edit/<int:pk>/<str:model_name>/<int:initial_id>/<str:success_url>', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('edit/<int:pk>/<str:model_name>/<str:initial_type>/<int:initial_id>/<str:success_url>/', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    # path('<int:pk>/delete/', InventoryItemDeleteView.as_view(), name='inventory_delete'),
    # path('<int:pk>/delete/<int:parent_id>', InventoryItemDeleteView.as_view(), name='inventory_delete'),
    # path('<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_detail'),
]