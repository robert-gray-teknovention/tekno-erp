from django.urls import path
from . import views

urlpatterns = [
    path('', views.timesheet_entries, name='timesheetentries'),
    path('report', views.report, name='report'),
    path('submitutp', views.submit_timesheet, name='submitutp'),
    path('timesheetperiod/<str:date_time_in>/', views.get_timesheet_period, name='get_timesheet_period'),
    ]
