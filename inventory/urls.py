from django.urls import path
from .views import (
    InventoryItemListView, InventoryItemListByItemIdView, InventoryItemCreateView,
    InventoryItemUpdateView, InventoryItemDeleteView, InventoryFilteredListView, get_items
)

urlpatterns = [
    path('', InventoryFilteredListView.as_view(), name='inventory_list'),
    path('<str:model_name>/', InventoryFilteredListView.as_view(), name='inventory_list'),
    path('item/<str:model_name>/<str:lookup_type>/<int:lookup_id>/', InventoryItemListView.as_view(), name='inventory_item_list'),
    path('item/<int:pk>/', InventoryItemListByItemIdView.as_view(), name='inventory_item_list'),
    path('add/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('add/<str:model_name>/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('add/<str:model_name>/<int:initial_id>/<success_url>/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('add/<str:model_name>/<str:initial_type>/<int:initial_id>/<str:success_url>/', InventoryItemCreateView.as_view(), name='inventory_add'),
    path('edit/', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('edit/<int:pk>', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('edit/<int:pk>/<str:model_name>/<int:initial_id>/<str:success_url>/', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('edit/<int:pk>/<str:model_name>/<str:initial_type>/<int:initial_id>/<str:success_url>/', InventoryItemUpdateView.as_view(), name='inventory_edit'),
    path('items/search/', get_items, name='search_inventory_items'),
    path('delete/<int:pk>/<str:model_name>/<int:initial_id>/<str:success_url>/', InventoryItemDeleteView.as_view(), name='inventory_delete'),
    # path('<int:pk>/delete/<int:parent_id>', InventoryItemDeleteView.as_view(), name='inventory_delete'),
    # path('<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_detail'),
]