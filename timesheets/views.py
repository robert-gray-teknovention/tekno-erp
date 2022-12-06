from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import TimesheetEntry
from employee.models import TimesheetUser
from .utils import TimesheetUtil
from django.utils import timezone
import pytz


def index(request):
    return render(request, 'index.html')


def timesheet_entries(request):
    if request.method == 'POST':
        util = TimesheetUtil()
        duration = request.POST['duration']
        ts_user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
        date_time_in = timezone.localtime(util.get_time_with_timezone(request.POST['date_time_in'], '%Y-%m-%dT%H:%M',
                                          ts_user.organization.timezone), pytz.timezone(ts_user.organization.timezone))
        entry = TimesheetEntry(user=ts_user, date_time_in=request.POST['date_time_in'],
                               date_time_out=request.POST['date_time_out'], duration=duration)
        entry.notes = request.POST['notes']
        period = util.get_timesheet_period(date_time_in, ts_user.organization)
        entry.period = period
        entry.save()

        messages.success(request, 'Time Sheet Entry added successfully')

        return redirect('/accounts/dashboard')
