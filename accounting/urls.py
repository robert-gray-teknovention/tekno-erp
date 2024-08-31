from django.urls import path
from . import views
# from .views import VendorListView

urlpatterns = [
    path('expense/<str:type>/', views.expense, name='expense'),
    path('expense/<str:type>/<int:id>', views.expense, name='expense'),
    path('expenses/', views.ExpenseListView.as_view()),
    path('expenses/<str:group>/<int:id>', views.ExpenseListView.as_view()),
    path('expenses/<str:group>/<int:id>/<str:partial>/', views.ExpenseListView.as_view()),
    # path('manufacturer', views.company, name='company'),
    # path('vendors', views.FilteredCompanyListView.as_view()),
    # path('manufacturers', views.FilteredCompanyListView.as_view()),
    # path('api/company', views.CompanyApiView, name='api_company')
    ]
