from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employee.urls')),
    path('timesheetentries/', include('timesheets.urls')),
    path('accounts/', include('accounts.urls')),
    path('manage/', include('tsmanagement.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('message/', include('mailer.urls')),
    path('purchasing/', include('purchasing.urls')),
    path('demo', TemplateView.as_view(template_name="bootstrap_base.html"), name='demo'),
    path('popovers', TemplateView.as_view(template_name="bootstrap_popovers.html"), name="popovers"),
]
