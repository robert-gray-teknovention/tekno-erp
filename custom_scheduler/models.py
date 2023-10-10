from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization
from schedule.models.events import Event as BaseEvent, Occurrence
from schedule.models.calendars import Calendar as BaseCalendar
from schedule.utils import OccurrenceReplacer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
from django.utils import timezone
import pytz
import datetime as dt
# Create your models here.


class Calendar(BaseCalendar):
    organization = models.ForeignKey(Organization, related_name='calendars', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    # Future of shared organizations


class EventType(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    color_event = models.CharField(_("Color event"), blank=True, max_length=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'organization'], name='name_organization_constraint')
        ]

    def __str__(self):
        return self.name


class CustomEvent(BaseEvent):
    '''class EventType(models.TextChoices):
        BP = 'BP', 'Birthday Party'
        OP = 'OP', 'Open Play'
        SC = 'SC', 'Summer Camp'
        CP = 'CP', 'Crafter Play'
        FT = 'FT', 'Field Trip'
        OR = 'OR', 'Outreach'
    '''
    event_type = models.ForeignKey(EventType, null=True, on_delete=models.SET_NULL)
    duration = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        delta = (self.end - self.start)
        self.duration = delta/dt.timedelta(hours=1)
        super(CustomEvent, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        Occurrence.objects.filter(event=self.id).delete()
        super(CustomEvent, self).delete(*args, **kwargs)

    # Had to override get occurrence method because doesn't work with timezones and such
    def get_occurrence(self, date):
        naive_date = date
        use_naive = timezone.is_naive(date)
        tzinfo = datetime.timezone.utc
        if timezone.is_naive(date):
            date = timezone.make_aware(date, tzinfo)
        if date.tzinfo:
            tzinfo = date.tzinfo
        if timezone.is_naive(self.start):
            start = timezone.make_aware(self.start, tzinfo)
        rule = self.get_rrule_object(tzinfo)
        if rule:
            next_occurrence = rule.after(
                date.astimezone(tzinfo).replace(tzinfo=None), inc=True
            )
            next_occurrence = pytz.timezone(str(tzinfo)).localize(next_occurrence)
        else:
            next_occurrence = start
        if next_occurrence == date:
            try:
                return Occurrence.objects.get(event=self, original_start=naive_date)
            except Occurrence.DoesNotExist:
                if use_naive:
                    next_occurrence = timezone.make_naive(next_occurrence, tzinfo)
                return self._create_occurrence(next_occurrence)

    def __str__(self):
        return self.title


class Staff(models.Model):
    class StaffType(models.TextChoices):
        HRL = "HRL", "Hourly Employee"
        SAL = "SAL", "Salary Employee"
        VOL = "VOL", "Volunteer"
        TEM = "TEM", "Temporary"
        BRD = "BRD", "Board Member"

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20, null=True)
    staff_type = models.CharField(max_length=25, choices=StaffType.choices)
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class StaffTime(models.Model):
    staff_member = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField(auto_now=False)
    end = models.DateTimeField(auto_now=False)
    event = models.ForeignKey(BaseEvent, on_delete=models.CASCADE, null=True)
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE, related_name="staffing", null=True)
    occ_start = ''
    occ_end = ''

    def __str__(self):
        return str(self.staff_member) + 'Start: ' + str(self.start) + ' End: ' + str(self.end)

    def clean(self):
        if self.start and self.end and self.start > self.end:
            raise ValidationError(_("Start time cannot be later than end time."))

    def add_occurrence(self):
        # the event parameter in this case is a base event
        # Check to see if occurrence exists.  If not then create the occurrence and add the StaffTime
        occ = Occurrence(event=self.event, start=self.occ_start, end=self.occ_end,
                         original_start=self.occ_start, original_end=self.occ_end)
        occ.save()
        self.occurrence = occ
        self.save()
