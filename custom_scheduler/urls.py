from custom_scheduler.views import EventViewAddChangeDelete, api_occurrences
from django.urls import re_path

urlpatterns = [
    re_path(r'^event/api/', EventViewAddChangeDelete.as_view(), name='event_api'),
    re_path(r"^api/occurrences", api_occurrences, name="api_occurrences"),
]
