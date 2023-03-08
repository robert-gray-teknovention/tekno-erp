from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime, timedelta
from dateutil import relativedelta
import pytz
# Create your models here.


class Organization(models.Model):
    def get_tuple_timezones(tzs):
        timezones = []
        for tz in tzs:
            timezones.append([tz, tz])
        return tuple(timezones)
    name = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    phone = models.CharField(max_length=20)
    mailer_email = models.EmailField(max_length=255)
    timezone = models.CharField(max_length=50, blank=True, null=True, default='America/Los_Angeles',
                                choices=get_tuple_timezones(pytz.common_timezones)
                                )

    def __str__(self):
        return self.name


class PeriodType(models.Model):
    types = (
        ('semimonthly', 'SEMI-MONTHLY'),
        ('monthly', 'MONTHLY'),
        ('biweekly', 'BI-WEEKLY'),
        ('weekly', 'WEEKLY')
    )
    periods_in_year = {
        'SEMI-MONTHLY': 24,
        'MONTHLY': 12,
        'BI-WEEKLY': 26,
        'WEEKLY': 52
    }
    name = models.CharField(max_length=20, choices=types)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    seed_date = models.DateTimeField(auto_now=False, auto_now_add=False,
                                     help_text='This field is only used if name is weekly or biweekly')
    dates_of_month = ArrayField(models.IntegerField(), size=2, help_text='Only used with semi-monthly')

    def __str__(self):
        return self.name

    def get_start_and_end_date(self, tz):
        timezone = pytz.timezone(tz)
        if (self.name == self.types[2][0]):
            date_start = self.seed_date
            date_end = self.seed_date + timedelta(weeks=2)
            if(datetime.now(timezone) > self.seed_date):
                self.seed_date = date_start + timedelta(weeks=2)
                self.save()
            return {
                'date_start': date_start,
                'date_end': date_end
                }
        if (self.name == self.types[0][0]):
            if (datetime.now(timezone).day >= self.dates_of_month[1]):
                return {
                    'date_start': datetime.now().replace(day=self.dates_of_month[1]).replace(
                        hour=self.seed_date.hour).replace(minute=self.seed_date.minute).replace(
                        second=self.seed_date.second).replace(microsecond=0),
                    'date_end': datetime.now().replace(
                        hour=self.seed_date.hour).replace(minute=self.seed_date.minute).replace(
                        second=self.seed_date.second).replace(microsecond=0) +
                    relativedelta.relativedelta(months=1, day=self.dates_of_month[0])
                    }
            else:
                return {
                    'date_start': datetime.now().replace(day=self.dates_of_month[0]).replace(
                        hour=self.seed_date.hour).replace(minute=self.seed_date.minute).replace(
                        second=self.seed_date.second).replace(microsecond=0),
                    'date_end': datetime.now().replace(day=self.dates_of_month[1]).replace(
                        hour=self.seed_date.hour).replace(minute=self.seed_date.minute).replace(
                        second=self.seed_date.second).replace(microsecond=0)
                    }
        if (self.name == self.types[1][0]):
            return {
                'date_start': datetime.now().replace(day=self.dates_of_month[0]).replace(
                    hour=self.seed_date.hour).replace(minute=self.seed_date.minute).replace(
                    second=self.seed_date.second).replace(microsecond=0),
                'date_end': datetime.now().replace(
                    hour=self.seed_date.hour).replace(minute=self.seed_date.minute).replace(
                    second=self.seed_date.second).replace(microsecond=0) +
                relativedelta.relativedelta(months=1, day=self.dates_of_month[0])
                }
