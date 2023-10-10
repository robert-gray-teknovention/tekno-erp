from django.contrib import admin
from custom_scheduler.models import CustomEvent, Staff, StaffTime, EventType
from custom_scheduler.forms import CustomEventAdminForm, EventTypeAdminForm
from schedule.models import Occurrence
from schedule.admin import EventAdmin
# Register your models here.


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')


class StaffTimeAdminInline(admin.TabularInline):
    model = Occurrence


@admin.register(StaffTime)
class StaffTime(admin.ModelAdmin):
    list_display = ('start', 'end')


@admin.register(CustomEvent)
class CustomEventAdmin(EventAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": [
                    ("title", "event_type", "color_event"),
                    ("description",),
                    ("start", "end", "duration"),
                    ("creator", "calendar"),
                    ("rule", "end_recurring_period"),

                ]
            },
        ),
    )
    inlines = (StaffTimeAdminInline,)
    form = CustomEventAdminForm


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    list_display = ('name', 'organization', 'color_event')
    form = EventTypeAdminForm
