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
        if 'addOrUpdateBtn' in request.POST:
            entry = {}
            util = TimesheetUtil()
            duration = request.POST['duration']
            ts_user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
            date_time_in = timezone.localtime(util.get_time_with_timezone(request.POST['date_time_in'],
                                              '%Y-%m-%dT%H:%M', ts_user.organization.timezone),
                                              pytz.timezone(ts_user.organization.timezone))
            period = util.get_timesheet_period(date_time_in, ts_user.organization)
            if int(request.POST['id']) > 0:
                entry = TimesheetEntry.objects.get(id=int(request.POST['id']))
                entry.user = ts_user
                entry.date_time_in = request.POST['date_time_in']
                entry.date_time_out = request.POST['date_time_out']
                entry.duration = request.POST['duration']
                entry.notes = request.POST['notes']
            else:
                entry = TimesheetEntry(user=ts_user, date_time_in=request.POST['date_time_in'],
                                       date_time_out=request.POST['date_time_out'], duration=duration,
                                       notes=request.POST['notes'])
                entry.period = period
            if period.id == entry.period.id:
                entry.save()
                messages.success(request, 'Time Sheet Entry was saved successfully')
            else:
                messages.error(request, 'This entry was not saved because it is not in the same timesheet period.')
            return redirect('/accounts/dashboard')
        elif 'deleteBtn' in request.POST:
            if int(request.POST['id']) > 0:
                entry = TimesheetEntry.objects.get(id=int(request.POST['id']))
                entry.delete()
                messages.success(request, "Your timesheet entry was deleted successfully")
            else:
                messages.error(request, 'There was no timesheet entry to delete')
            return redirect('/accounts/dashboard')
