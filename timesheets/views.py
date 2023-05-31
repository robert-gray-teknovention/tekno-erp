from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import TimesheetEntry, TimesheetPeriod, UserTimesheetPeriod
from employee.models import TimesheetUser
from .utils import TimesheetUtil
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from django.http import FileResponse
import datetime
import io
import pytz


def index(request):
    return render(request, 'index.html')


def timesheet_entries(request):
    if request.method == 'POST':
        if str(request.POST['utp_approved']) == 'False' and str(request.POST['utp_submitted'] == 'False'):
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
                    entry.hourly_rate = ts_user.hourly_rate
                else:
                    entry = TimesheetEntry(user=ts_user, date_time_in=request.POST['date_time_in'],
                                           date_time_out=request.POST['date_time_out'], duration=duration,
                                           notes=request.POST['notes'], hourly_rate=ts_user.hourly_rate)
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
        else:
            messages.error(request,
                           'No changes to the timesheet has been made. Timesheet is either submitted or approved')
    return redirect('/accounts/dashboard')


def submit_timesheet(request):
    id = request.POST['utp_id']
    utp = UserTimesheetPeriod.objects.get(id=id)
    if utp.approved:
        messages.error(request, "Sorry but your timesheet is locked because it is approved.")
    else:
        if utp.submitted:
            utp.submitted = False
            utp.date_submitted = None
            messages.success(request, "You have (un)submitted your timesheet!")
        else:
            utp.submitted = True
            utp.date_submitted = datetime.datetime.now()
            messages.success(request, "You have submitted your timesheet!")
        utp.save()
    return redirect('/accounts/dashboard')


def report(request):
    user_ids = [request.user.id]
    buffer = get_report(user_ids, request.GET.get("period_id"), True)
    return FileResponse(buffer, as_attachment=False, filename='report.pdf')


def get_report(user_ids, period_id, show_notes):
    period = TimesheetPeriod.objects.get(id=period_id)
    buffer = io.BytesIO()
    deltay = 15
    p = canvas.Canvas(buffer)
    for user_id in user_ids:
        x1 = 20
        y1 = 750
        user = TimesheetUser.objects.get(user=User.objects.get(id=user_id))
        entries = TimesheetEntry.objects.filter(user=user, period=period)
        aggregate_data = {'total_hours': 0.00, 'total_pay': 0.00}
        p.setPageSize(portrait(letter))
        p.setFont("Helvetica", 15, leading=None)
        p.drawString(x1, y1, "Timesheet Report for " + user.organization.name)
        p.drawString(x1, y1-15, "Employee: " + user.user.first_name + " " + user.user.last_name)
        p.drawString(x1, y1-40, "Pay Period: " + str(period))
        p.drawString(x1, y1-60, "Timesheet Entries")
        p.setFont("Courier", 12, leading=None)
        x1 += 5
        y1 -= 80
        column_headers = [{'width': 125, 'text': 'Time In'},
                          {'width': 125, 'text': 'Time Out'},
                          {'width': 80, 'text': 'Rate/Hr'},
                          {'width': 90, 'text': 'Duration'},
                          {'width': 60, 'text': 'Pay'},

                          ]
        for ch in column_headers:
            p.drawString(x1, y1, ch['text'])
            x1 += ch['width']
        x1 = 20
        y1 -= 5
        p.line(x1, y1, x1+500, y1)
        y1 -= deltay
        for e in entries:
            pay = float(e.hourly_rate) * float(e.duration)
            aggregate_data['total_hours'] += float(e.duration)
            aggregate_data['total_pay'] += pay
            x1 = 25
            earray = [datetime.date.strftime(e.date_time_in, "%m-%d-%Y %H:%M"),
                      datetime.date.strftime(e.date_time_out, "%m-%d-%Y %H:%M"), '{:.2f}'.format(e.hourly_rate),
                      str(e.duration), '{:.2f}'.format(pay)]
            i = 0
            p.setFont("Courier", 10, leading=None)
            for ch in column_headers:
                p.drawString(x1, y1, earray[i])
                x1 += ch['width']
                i += 1
            y1 -= deltay
        x1 = 20
        p.line(x1, y1, x1+500, y1)
        y1 += 3
        p.line(x1, y1, x1+500, y1)
        x1 = 25
        x1 += column_headers[0]['width'] + column_headers[1]['width']
        y1 -= deltay
        p.drawString(x1, y1, "Total")
        x1 += column_headers[2]['width']
        p.drawString(x1, y1, '{:.2f}'.format(aggregate_data['total_hours']))
        x1 += column_headers[3]['width']
        p.drawString(x1, y1, '{:.2f}'.format(aggregate_data['total_pay']))
        if (show_notes):
            p.showPage()
            x1 = 25
            y1 = 750
            p.setFont("Helvetica", 15, leading=None)
            p.drawString(x1, y1, "Timesheet Entry Notes")
            y1 -= 60
            styleSheet = getSampleStyleSheet()
            style = styleSheet['BodyText']
            aW = 500    # available width and height
            aH = 725
            for e in entries:
                in_time = datetime.date.strftime(e.date_time_in, "%m-%d-%Y %H:%M")
                out_time = datetime.date.strftime(e.date_time_out, "%m-%d-%Y %H:%M")
                par = Paragraph(in_time + " - " + out_time + ":  " + str(e.notes), style)
                w, h = par.wrap(aW, aH)    # find required space
                if w <= aW and 2 * h <= aH:
                    aH = aH - h - 20       # reduce the available height
                    par.drawOn(p, x1, aH)
                else:
                    aH = 725
                    p.showPage()
                    par.drawOn(p, x1, aH)
        p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
