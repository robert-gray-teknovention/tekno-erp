from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import TimesheetEntry
from employee.models import TimesheetUser


def index(request):
    return render(request, 'index.html')


def timesheet_entries(request):
    if request.method == 'POST':
        date_time_in = request.POST['date_time_in']
        date_time_out = request.POST['date_time_out']
        duration = request.POST['duration']
        ts_user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
        entry = TimesheetEntry(user=ts_user, date_time_in=date_time_in, date_time_out=date_time_out,
                               duration=duration)
        entry.save()

        messages.success(request, 'Time Sheet Entry added successfully')

        return redirect('/accounts/dashboard')
