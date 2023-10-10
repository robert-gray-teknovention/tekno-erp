from schedule.forms import EventAdminForm
from schedule.widgets import ColorInput
from custom_scheduler.models import CustomEvent, StaffTime, EventType

# from django.contrib.admin.widgets import AdminDateWidget
from django import forms
# from django.forms import DateTimeField


class CustomEventAdminForm(EventAdminForm):

    class Meta:
        model = CustomEvent
        fields = "__all__"
        widgets = {"color_event": ColorInput}


class EventTypeAdminForm(forms.ModelForm):
    class Meta:
        model = EventType
        exclude = []
        widgets = {"color_event": ColorInput}


class CustomEventForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    field_order = ['start_time', 'end_time']

    class Meta:
        exclude = ('duration', 'creator')
        fields = "__all__"
        model = CustomEvent
        widgets = {
            'start': forms.DateTimeInput(attrs={'class': 'timepicker', 'type': 'datetime-local'}),
            'end': forms.DateTimeInput(attrs={'class': 'timepicker', 'type': 'datetime-local'}),
            'end_recurring_period': forms.DateTimeInput(attrs={'class': 'timepicker', 'type': 'datetime-local'}),
            'color_event': ColorInput
        }


class StaffTimeForm(forms.ModelForm):

    class Meta:
        exclude = ['event', 'occurrence']
        fields = "__all__"
        model = StaffTime
        widgets = {
            'start': forms.DateTimeInput(attrs={'class': 'timepicker', 'type': 'datetime-local'}),
            'end': forms.DateInput(attrs={'class': 'timepicker', 'type': 'datetime-local'})
        }
