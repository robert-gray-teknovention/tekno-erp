from django.urls import path
from . import views

urlpatterns = [
    path('', views.timesheet_entries, name='timesheetentries')
    ]
