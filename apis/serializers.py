# import serializer from rest_framework
from rest_framework import serializers
from django.contrib.auth.models import User
from custom_scheduler.models import CustomEvent, Calendar, EventType, Staff, StaffTime
from organizations.models import Organization
from schedule.models.events import Occurrence, Event as BaseEvent, Calendar as BaseCalendar
from schedule.models.rules import Rule


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = 'url', 'id', 'first_name', 'last_name', 'email'


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Organization
        fields = ('__all__')


class GetCalendarSerializer(serializers.HyperlinkedModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = Calendar
        fields = ('url', 'id', 'name', 'slug', 'organization')


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ('__all__')


class BaseCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseCalendar
        fields = ('__all__')


class RuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rule
        fields = ('url', 'id', 'name', 'description', 'frequency', 'params')


class BaseEventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BaseEvent
        fields = ('url', 'id', 'title', 'description', 'start', 'end', 'calendar')


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventType
        fields = ('url', 'id', 'name', 'organization', 'color_event')


class CustomEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomEvent
        fields = ('__all__')


class GetCustomEventSerializer(serializers.HyperlinkedModelSerializer):
    calendar = BaseCalendarSerializer()
    event_type = EventTypeSerializer()
    rule = RuleSerializer()

    class Meta:
        model = CustomEvent
        fields = ('__all__')


class StaffSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staff
        fields = ('url', 'id', 'user', 'name', 'email', 'phone', 'staff_type', 'organization')


class StaffTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTime
        fields = ('__all__')


class GetStaffTimeSerializer(serializers.HyperlinkedModelSerializer):
    staff_member = StaffSerializer()

    class Meta:
        model = StaffTime
        fields = ('url', 'id', 'staff_member', 'start', 'end', 'event', 'occurrence')


class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = ('url', 'event', 'title', 'description', 'start', 'end', 'original_start', 'original_end',
                  'created_on',
                  'updated_on',
                  'staffing')


class GetOccurrenceSerializer(serializers.HyperlinkedModelSerializer):
    staffing = GetStaffTimeSerializer(many=True)

    class Meta:
        model = Occurrence
        fields = ('__all__')
