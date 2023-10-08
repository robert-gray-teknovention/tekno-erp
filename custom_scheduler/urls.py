from custom_scheduler.views import EventViewAddChangeDelete
from django.urls import re_path

urlpatterns = [
    re_path(r'^event/api/', EventViewAddChangeDelete.as_view(), name='event_api'),
]
