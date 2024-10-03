from django.urls import path
from . import views
# from .views import VendorListView

urlpatterns = [
    path('company', views.company, name='company'),
    # path('manufacturer', views.company, name='company'),
    path('vendors', views.FilteredCompanyListView.as_view()),
    path('manufacturers', views.FilteredCompanyListView.as_view()),
    path('api/company', views.CompanyApiView, name='api_company'),
    path('dashboard/', views.dashboard, name='purchasing-dashboard'),
    path('purchaseorders/', views.PurchaseOrderListView.as_view()),
    path('purchaseorder/create/', views.PurchaseOrderCreateView.as_view(), name='po-create'),
    path('purchaseorder/<int:pk>/update/', views.PurchaseOrderUpdateView.as_view(), name='po-update'),
    path('purchaseorderitem/create/', views.PurchaseOrderItemCreateView.as_view(), name='poi-create'),
    # path('purchaseorder/<int:id>/delete/', views.PurchaseOrderDeleteView.as_view(), name='po-delete'),
    # path('purchaseorders/<int:id>', )
    ]
