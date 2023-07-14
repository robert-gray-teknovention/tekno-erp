from django.urls import path
from . import views

urlpatterns = [
    path('managedashboard', views.managedashboard, name='managedashboard'),
    path('tsapprovals', views.tsapprovals, name='tsapprovals'),
    path('report', views.report, name='managereport'),
    path('report_approvee', views.report_approvee, name='reportapprovee'),
    path('onboarding', views.onboarding, name='onboarding')
    ]
