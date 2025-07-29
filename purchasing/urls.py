from django.urls import path
from . import views
# from .views import VendorListView

urlpatterns = [
    path('company', views.company, name='company'),
    # path('manufacturer', views.company, name='company'),
    path('<str:template>/vendors', views.FilteredListView.as_view(), name='vendors'),
    path('<str:template>/manufacturers', views.FilteredListView.as_view(), name='manufacturers'),
    path('api/company', views.CompanyApiView, name='api_company'),
    path('dashboard/', views.dashboard, name='purchasing-dashboard'),
    path('purchaseorders/', views.PurchaseOrderListView.as_view(), name='po-list'),
    path('purchaseorder/create/', views.PurchaseOrderCreateView.as_view(), name='po-create'),
    path('purchaseorder/<int:pk>/update/', views.PurchaseOrderUpdateView.as_view(), name='po-update'),
    path('purchaseorderitem/create/', views.PurchaseOrderItemCreateView.as_view(), name='poi-create'),
    path('purchaseorderitem/<int:pk>/update/', views.PurchaseOrderItemUpdateView.as_view(), name='poi-update'),
    path('items/search/', views.get_items, name='search-items'),
    # path('purchaseorderitemform/', )
    path('purchaseorderitem/', views.PurchaseOrderItemUpdateView.as_view(), name='poi-form'),
    path('purchaseorderitem/<int:pk>', views.PurchaseOrderItemUpdateView.as_view(), name='poi-form'),
    path('<str:template>/parts', views.FilteredListView.as_view(), name='parts'),
    path('<str:template>/materials', views.FilteredListView.as_view(), name='materials'),
    path('<str:template>/foods', views.FilteredListView.as_view(), name='foods'),
    path('<str:template>/subscriptions', views.FilteredListView.as_view(), name='subscriptions'),
    path('<str:template>/services', views.FilteredListView.as_view(), name='services'),
    path('item/create/', views.ItemCreateView.as_view(), name='item-form'),
    path('item/create/<str:item_type>', views.ItemCreateView.as_view(), name='item-create-form'),
    path('item/create/<str:item_type>/list/', views.ItemCreateViewList.as_view(), name='item-create-formlist'),
    path('item/update/<str:item_type>/<int:pk>', views.ItemUpdateView.as_view(), name='item-update-form'),
    path('item/update/<str:item_type>/<int:pk>/list/', views.ItemUpdateViewList.as_view(), name='item-update-formlist'),

    # path('purchaseorder/<int:id>/delete/', views.PurchaseOrderDeleteView.as_view(), name='po-delete'),
    # path('purchaseorders/<int:id>', )
    ]
