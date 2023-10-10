from django.contrib import admin
# from django.urls import path, include
from django.views.generic.base import TemplateView
from custom_scheduler.views import CalendarView
from django.conf.urls import include
from django.urls import path, re_path
from django.conf import settings

urlpatterns = [
    path('', include('employee.urls')),
    path('timesheetentries/', include('timesheets.urls')),
    path('accounts/', include('accounts.urls')),
    path('manage/', include('tsmanagement.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('message/', include('mailer.urls')),
    path('purchasing/', include('purchasing.urls')),
    path('demo', TemplateView.as_view(template_name="bootstrap_base.html"), name='demo'),
    path('popovers', TemplateView.as_view(template_name="bootstrap_popovers.html"), name="popovers"),
    re_path(r'^schedule/', include('schedule.urls')),
    re_path(r'^fullcalendar/', CalendarView.as_view(template_name="fullcalendar.html"), name='fullcalendar'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^customschedule/', include('custom_scheduler.urls')),
    path('apis/', include('apis.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
