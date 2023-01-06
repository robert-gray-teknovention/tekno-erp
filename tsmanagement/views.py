from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from timesheets.models import TimesheetEntry, TimesheetPeriod
from tsmanagement.models import Approval
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
    approvees = user.approvees.all()
    user_time_entries = TimesheetEntry.objects.order_by('-date_time_out').filter(period_id=query_period['id'],
                                                                                 user__in=approvees)
    for entry in user_time_entries:
        if (entry.approvals.filter(approver=user)):
            entry.approver_approved = True
    users = TimesheetUser.objects.all()
    context = {
        'time_entries': user_time_entries,
        'periods': periods,
        'selected_period': query_period['id'],
        'users': users
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
        messages.success(request, "Your approvals have been successfully saved!")
        return redirect("/manage/managedashboard?period_id=" + request.POST.get("period_id"))
