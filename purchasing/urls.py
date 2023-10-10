from django.urls import path
from . import views
# from .views import VendorListView

urlpatterns = [
    path('company', views.company, name='company'),
    # path('manufacturer', views.company, name='company'),
    path('vendors', views.FilteredCompanyListView.as_view()),
    path('manufacturers', views.FilteredCompanyListView.as_view()),
    path('api/company', views.CompanyApiView, name='api_company')
    ]
