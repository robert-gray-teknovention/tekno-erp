from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from timesheets.models import TimesheetEntry, TimesheetPeriod
from employee.models import TimesheetUser
from django.contrib.auth.decorators import permission_required
from datetime import date
import pytz


@permission_required("timesheets.approve_timesheetentry", raise_exception=True)
def managedashboard(request):
    periods = []
    user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
    tz = pytz.timezone(user.organization.timezone)
    for p in TimesheetPeriod.objects.filter(org=user.organization).order_by('-date_end')[0:12]:
        periods.append({'id': p.id, 'date_start': date.strftime(timezone.localtime(p.date_start, tz), '%m/%d/%Y'),
                       'date_end': date.strftime(timezone.localtime(p.date_end, tz), '%m/%d/%Y')})
    query_period = periods[0]
    if request.GET.get('period_id'):
        p = TimesheetPeriod.objects.get(id=request.GET.get('period_id'))
        query_period = {'id': p.id, 'date_start': date.strftime(timezone.localtime(p.date_start, tz), '%m/%d/%Y'),
                        'date_end': date.strftime(timezone.localtime(p.date_end, tz), '%m/%d/%Y')}
    user_time_entries = TimesheetEntry.objects.order_by('-date_time_out').filter(period_id=query_period['id'])
    users = TimesheetUser.objects.all()
    context = {
        'time_entries': user_time_entries,
        'periods': periods,
        'selected_period': query_period['id'],
        'users': users
    }

    return render(request, 'tsmanagement/managedashboard.html', context)
