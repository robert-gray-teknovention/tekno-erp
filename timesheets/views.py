from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import TimesheetEntry, TimesheetPeriod
from employee.models import TimesheetUser
from .utils import TimesheetUtil
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from django.http import FileResponse
import datetime
import io
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


def report(request):
    user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
    period = TimesheetPeriod.objects.get(id=request.GET.get("period_id"))
    entries = TimesheetEntry.objects.filter(user=user, period=period)
    aggregate_data = {}

    buffer = io.BytesIO()
    x1 = 20
    y1 = 575
    deltay = 15
    p = canvas.Canvas(buffer)
    p.setPageSize(landscape(letter))
    p.setFont("Helvetica", 15, leading=None)
    p.drawString(x1, y1, "Timesheet Report: " + user.user.first_name + " " + user.user.last_name)
    p.drawString(x1, y1-15, "Pay Period: " + str(period))
    p.drawString(x1, y1-40, "Timesheet Entries")
    p.setFont("Courier", 12, leading=None)
    x1 += 5
    y1 -= 60
    column_headers = [{'width': 125, 'text': 'Time In'},
                      {'width': 125, 'text': 'Time Out'},
                      {'width': 90, 'text': 'Duration'},
                      {'width': 60, 'text': 'Pay'},
                      {'width': 100, 'text': 'Notes'},
                      ]
    for ch in column_headers:
        p.drawString(x1, y1, ch['text'])
        x1 += ch['width']
    y1 -= deltay
    for e in entries:
        x1 = 25
        earray = [datetime.date.strftime(e.date_time_in, "%m-%d-%Y %H:%M"),
                  datetime.date.strftime(e.date_time_out, "%m-%d-%Y %H:%M"), str(e.duration), "100.0", str(e.notes)]
        i = 0
        p.setFont("Courier", 10, leading=None)
        for ch in column_headers:
            p.drawString(x1, y1, earray[i])
            x1 += ch['width']
            i += 1
        y1 -= deltay
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=False, filename='report.pdf')
