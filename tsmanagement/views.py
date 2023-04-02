from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from timesheets.models import TimesheetEntry, TimesheetPeriod, UserTimesheetPeriod
from tsmanagement.models import Approval
from timesheets.views import get_report
from employee.models import TimesheetUser
from django.contrib.auth.decorators import permission_required
from datetime import date
from django.http import FileResponse
from mailer.forms import MailForm
import pytz


@permission_required("timesheets.approve_timesheetentry", raise_exception=True)
def managedashboard(request):
    periods = []
    user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
    tz = pytz.timezone(user.organization.timezone)
    tps = TimesheetPeriod.objects.filter(org=user.organization).order_by('-date_end')[0:12]
    for p in tps:
        periods.append({'id': p.id, 'date_start': date.strftime(timezone.localtime(p.date_start, tz), '%m/%d/%Y'),
                       'date_end': date.strftime(timezone.localtime(p.date_end, tz), '%m/%d/%Y')})
    query_period = periods[0]
    if request.GET.get('period_id'):
        p = TimesheetPeriod.objects.get(id=request.GET.get('period_id'))
        query_period = {'id': p.id, 'date_start': date.strftime(timezone.localtime(p.date_start, tz), '%m/%d/%Y'),
                        'date_end': date.strftime(timezone.localtime(p.date_end, tz), '%m/%d/%Y')}
    approvees = user.approvees.all()
    user_time_entries = TimesheetEntry.objects.order_by('user', '-date_time_in').filter(period_id=query_period['id'],
                                                                                        user__in=approvees)
    utps = UserTimesheetPeriod.objects.filter(period__id=query_period['id'], user__in=approvees).order_by('user')
    for utp in utps:
        utp.entries = user_time_entries.filter(user=utp.user)
        for entry in utp.entries:
            if (entry.approvals.filter(approver=user)):
                entry.approver_approved = True
    for entry in user_time_entries:
        if (entry.approvals.filter(approver=user)):
            entry.approver_approved = True
    users = TimesheetUser.objects.all()
    mailForm = MailForm()
    context = {
        'time_entries': user_time_entries,
        'periods': periods,
        'selected_period': query_period['id'],
        'users': users,
        'utps': utps,
        'organization': user.organization,
        'mailForm': mailForm
    }
    return render(request, 'tsmanagement/managedashboard.html', context)


@permission_required("timesheets.approve_timesheetentry", raise_exception=True)
def tsapprovals(request):
    if request.method == "POST":
        approver = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
        for id in request.POST.getlist("entry_id"):
            entry = TimesheetEntry.objects.get(id=id)
            if (id in request.POST.getlist("approveCheck")):
                if (Approval.objects.filter(timesheet_entry=entry, approver=approver, approvee=entry.user).count() ==
                   0):
                    approval = Approval()
                    approval.approver = approver
                    approval.approvee = entry.user
                    approval.timesheet_entry = entry
                    approval.save()
            else:
                apprs = Approval.objects.filter(timesheet_entry=entry, approver=approver, approvee=entry.user)
                if (apprs.count() > 0):
                    for a in apprs:
                        a.delete()
            apprs = Approval.objects.filter(timesheet_entry=entry)
            if (apprs.count() == entry.user.approvers.all().count()):
                entry.is_approved = True
            else:
                entry.is_approved = False
            entry.save()
        utp = UserTimesheetPeriod.objects.get(id=request.POST.get('utp_id'))
        for e in TimesheetEntry.objects.filter(user=utp.user.id, period=utp.period):
            utp.approved = False
            if not e.is_approved:
                break
            utp.approved = True
        utp.save()
        messages.success(request, "Your approvals have been successfully saved!")
        return redirect("/manage/managedashboard?period_id=" + request.POST.get("period_id"))


@permission_required("timesheets.approve_timesheetentry", raise_exception=True)
def report(request):
    manager = User.objects.get(id=request.user.id)
    user_ids = []
    users = TimesheetUser.objects.get(user=manager).approvees.all()
    for u in users:
        user_ids.append(u.user.id)
    buffer = get_report(user_ids, request.GET.get("period_id"), False)
    return FileResponse(buffer, as_attachment=False, filename='report.pdf')


@permission_required("timesheets.approve_timesheetentry", raise_exception=True)
def report_approvee(request):
    utp = UserTimesheetPeriod.objects.get(id=request.GET.get("utp_id"))
    print(utp.user.user.first_name, ' ', utp.period.id)
    buffer = get_report([utp.user.user.id], utp.period.id, False)
    return FileResponse(buffer, as_attachment=False, filename='report.pdf')
