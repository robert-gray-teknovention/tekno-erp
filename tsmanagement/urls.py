from django.urls import path
from . import views

urlpatterns = [
    path('managedashboard', views.managedashboard, name='managedashboard'),
    path('tsapprovals', views.tsapprovals, name='tsapprovals'),
    ]
