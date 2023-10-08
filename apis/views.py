from django.shortcuts import render
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from .serializers import (
    UserSerializer,
    RuleSerializer,
    CustomEventSerializer,
    GetCustomEventSerializer,
    CalendarSerializer,
    GetCalendarSerializer,
    OrganizationSerializer,
    EventTypeSerializer,
    StaffSerializer,
    StaffTimeSerializer,
    GetStaffTimeSerializer,
    OccurrenceSerializer,
    GetOccurrenceSerializer,
    BaseEventSerializer,
    )
from custom_scheduler.models import CustomEvent, EventType, Calendar, Staff, StaffTime
from schedule.models.events import Occurrence, Event as BaseEvent
from schedule.models.rules import Rule
from organizations.models import Organization
from rest_framework.response import Response
from rest_framework.decorators import action
from django.views.decorators.http import require_POST
from django.db.models import F, Q
from schedule.settings import (
    CHECK_EVENT_PERM_FUNC,
    CHECK_OCCURRENCE_PERM_FUNC,
)
from django.conf import settings
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
)
import datetime
from schedule.utils import (
    check_calendar_permissions,
)
import copy
import pytz


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class CustomEventViewSet(viewsets.ModelViewSet):
    queryset = CustomEvent.objects.all()
    serializer_class = GetCustomEventSerializer

    def get_serializer_class(self):
        # Use SerializerForGET for GET requests
        if self.request.method == 'GET':
            return GetCustomEventSerializer
        # Use SerializerForPOST for POST requests
        elif self.request.method == 'POST' or self.request.method == 'PUT':
            return CustomEventSerializer
        # Use the default serializer for other HTTP methods
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        # Override get_serializer to pass the request context to the serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)
    # serializer_class = CustomEventSerializer


class BaseEventViewSet(viewsets.ModelViewSet):
    queryset = BaseEvent.objects.all()
    serializer_class = BaseEventSerializer

    '''@action(detail=False, methods=['GET'], url_path='occurrence')
    def occurrence_detail(self, request, pk=None):
        event = self.get_object()
        serializer = BaseEventSerializer(, many=False, context={'request': request})
        return Response(serializer.data)'''


class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = GetCalendarSerializer

    def get_serializer_class(self):
        # Use SerializerForGET for GET requests
        if self.request.method == 'GET':
            return GetCalendarSerializer
        # Use SerializerForPOST for POST requests
        elif self.request.method == 'POST' or self.request.method == 'PUT':
            return CalendarSerializer
        # Use the default serializer for other HTTP methods
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        # Override get_serializer to pass the request context to the serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @action(detail=True, methods=['GET'], url_path='events_list')
    def events_list(self, request, pk=None):
        calendar = self.get_object()
        events = calendar.event_set.all()
        serializer = BaseEventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffTimeViewSet(viewsets.ModelViewSet):
    queryset = StaffTime.objects.all()
    serializer_class = GetStaffTimeSerializer

    def get_serializer_class(self):
        # Use SerializerForGET for GET requests
        if self.request.method == 'GET':
            return GetStaffTimeSerializer
        # Use SerializerForPOST for POST requests
        elif self.request.method == 'POST':
            return StaffTimeSerializer
        # Use the default serializer for other HTTP methods
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        # Override get_serializer to pass the request context to the serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = copy.copy(request.data)
        occ_exists = True
        try:
            Occurrence.objects.get(id=request.data['occurrence'])
        except Occurrence.DoesNotExist:
            data['occurrence'] = ''
            occ_exists = False
        serializer = StaffTimeSerializer(context={'request': request}, data=data)
        if serializer.is_valid():
            st = serializer.save()
            if not occ_exists:
                st.occ_start = data['occ_start']
                st.occ_end = data['occ_end']
                st.add_occurrence()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OccurrenceViewSet(viewsets.ModelViewSet):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer

    def get_serializer_class(self):
        # Use SerializerForGET for GET requests
        if self.request.method == 'GET':
            return GetOccurrenceSerializer
        # Use SerializerForPOST for POST requests
        elif self.request.method == 'POST':
            return OccurrenceSerializer
        # Use the default serializer for other HTTP methods
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        # Override get_serializer to pass the request context to the serializer
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


@require_POST
@check_calendar_permissions
def api_move_or_resize_by_code(request):
    response_data = {}
    user = request.user
    id = request.POST.get("id")
    existed = bool(request.POST.get("existed") == "true")
    delta = datetime.timedelta(minutes=int(request.POST.get("delta")))
    resize = bool(request.POST.get("resize", False))
    event_id = request.POST.get("event_id")

    response_data = _api_move_or_resize_by_code(
        user, id, existed, delta, resize, event_id
    )

    return JsonResponse(response_data)


def _api_move_or_resize_by_code(user, id, existed, delta, resize, event_id):
    response_data = {}
    response_data["status"] = "PERMISSION DENIED"

    if existed:
        occurrence = Occurrence.objects.get(id=id)
        occurrence.end += delta
        if not resize:
            occurrence.start += delta
        if CHECK_OCCURRENCE_PERM_FUNC(occurrence, user):
            occurrence.save()
            response_data["status"] = "OK"
    else:
        event = CustomEvent.objects.get(id=event_id)
        dts = 0
        dte = delta
        if not resize:
            event.start += delta
            dts = delta
        event.end = event.end + delta
        print("Start ", event.start)
        print("End ", event.end)
        if CHECK_EVENT_PERM_FUNC(event, user):
            event.save()
            print("num of occurrences ", event.occurrence_set.all().count())
            event.occurrence_set.all().update(
                original_start=F("original_start") + dts,
                original_end=F("original_end") + dte,
            )
            response_data["status"] = "OK"
    return response_data


@check_calendar_permissions
def api_occurrences(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    calendar_slug = request.GET.get("calendar_slug")
    org = Calendar.objects.get(slug=calendar_slug).organization

    try:
        # response_data = _api_occurrences(start, end, calendar_slug, timezone)
        response_data = _api_occurrences(start, end, calendar_slug, org.timezone)
    except (ValueError, Calendar.DoesNotExist) as e:
        return HttpResponseBadRequest(e)

    return JsonResponse(response_data, safe=False)


def _api_occurrences(start, end, calendar_slug, timezone):

    if not start or not end:
        raise ValueError("Start and end parameters are required")
    # version 2 of full calendar
    # TODO: improve this code with date util package
    '''if "-" in start:

        def convert(ddatetime):
            if ddatetime:
                ddatetime = ddatetime.split(" ")[0]
                try:
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%d")
                except ValueError:
                    # try a different date string format first before failing
                    return datetime.datetime.strptime(ddatetime, "%Y-%m-%dT%H:%M:%S")

    else:

        def convert(ddatetime):
            return datetime.datetime.utcfromtimestamp(float(ddatetime)) '''

    start = datetime.datetime.fromisoformat(start)
    end = datetime.datetime.fromisoformat(end)
    current_tz = False
    if timezone and timezone in pytz.common_timezones:
        # make start and end dates aware in given timezone
        current_tz = pytz.timezone(timezone)
        start = current_tz.localize(start)
        end = current_tz.localize(end)
    elif settings.USE_TZ:
        # If USE_TZ is True, make start and end dates aware in UTC timezone
        utc = pytz.UTC
        start = utc.localize(start)
        end = utc.localize(end)

    if calendar_slug:
        # will raise DoesNotExist exception if no match
        calendars = [Calendar.objects.get(slug=calendar_slug)]
    # if no calendar slug is given, get all the calendars
    else:
        calendars = Calendar.objects.all()
    response_data = []
    # Algorithm to get an id for the occurrences in fullcalendar (NOT THE SAME
    # AS IN THE DB) which are always unique.
    # Fullcalendar thinks that all their "events" with the same "event.id" in
    # their system are the same object, because it's not really built around
    # the idea of events (generators)
    # and occurrences (their events).
    # Check the "persisted" boolean value that tells it whether to change the
    # event, using the "event_id" or the occurrence with the specified "id".
    # for more info https://github.com/llazzaro/django-scheduler/pull/169
    i = 1
    if Occurrence.objects.all().exists():
        i = Occurrence.objects.latest("id").id + 1
    event_list = []
    for calendar in calendars:
        # create flat list of events from each calendar
        event_list += calendar.events.filter(start__lte=end).filter(
            Q(end_recurring_period__gte=start) | Q(end_recurring_period__isnull=True)
        )
    for event in event_list:
        occurrences = event.get_occurrences(start, end)
        for occurrence in occurrences:
            occurrence_id = i + occurrence.event.id
            existed = False

            if occurrence.id:
                occurrence_id = occurrence.id
                existed = True

            recur_rule = occurrence.event.rule.name if occurrence.event.rule else None

            if occurrence.event.end_recurring_period:
                recur_period_end = occurrence.event.end_recurring_period
                if current_tz:
                    # make recur_period_end aware in given timezone
                    recur_period_end = recur_period_end.astimezone(current_tz)
                recur_period_end = recur_period_end
            else:
                recur_period_end = None

            event_start = occurrence.start
            event_end = occurrence.end
            if current_tz:
                # make event start and end dates aware in given timezone
                event_start = event_start.astimezone(current_tz)
                event_end = event_end.astimezone(current_tz)
            if occurrence.cancelled:
                # fixes bug 508
                continue
            response_data.append(
                {
                    "id": occurrence_id,
                    "title": occurrence.title,
                    "start": event_start,
                    "end": event_end,
                    "existed": existed,
                    "event_id": occurrence.event.id,
                    "color": occurrence.event.color_event,
                    "description": occurrence.description,
                    "rule": recur_rule,
                    "end_recurring_period": recur_period_end,
                    "creator": str(occurrence.event.creator),
                    "calendar": occurrence.event.calendar.slug,
                    "cancelled": occurrence.cancelled,
                }
            )
    return response_data
