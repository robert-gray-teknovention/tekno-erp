from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from timesheets.models import TimesheetEntry, TimesheetPeriod, UserTimesheetPeriod
from tsmanagement.models import Approval
from timesheets.views import get_report
from employee.models import TimesheetUser, Invitee
from employee.tables import InviteeTable
from django.contrib.auth.decorators import permission_required
from datetime import date
from django.http import FileResponse
from mailer.forms import MailForm
from mailer.utils import Emailer
from .forms import InviteeForm
import random
import string
import pytz
import environ


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


@permission_required(["employee.add_invitee"], raise_exception=True)
def onboarding(request):
    env = environ.Env()
    form = InviteeForm()

    if request.method == 'POST':
        inviter = TimesheetUser.objects.get(user=request.user)
        mailer = Emailer()
        invitee = Invitee()
        invitee.authentication_code = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _
                                              in range(10))
        invitee.organization = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id)).organization
        invitee.status = Invitee.Status.INVITED
        invitee.inviter = inviter

        f = InviteeForm(request.POST, instance=invitee)
        if f.is_valid():
            f.save()
            # Build email for Invitee
            subject = invitee.name + ' has been invited to join ' + invitee.organization.name + ' application.'
            message = 'Dear ' + invitee.name + ',\n\n'
            message += 'Please click on the link below and use the access code:  ' + invitee.authentication_code + '\n'
            message += env('BASE_URL') + 'accounts/register?org=' + str(invitee.organization.id)
            message += '\n Thank you for joining our organization'
            sender = inviter.user.email
            send_to = [invitee.email]
            reply_tos = [inviter.user.email]
            organization = invitee.organization
            mailer.send_and_log_mail(subject, message, sender, send_to, reply_tos,
                                     organization=organization)
            # Build email for Inviter
            message = 'Hello ' + inviter.user.first_name + ',\n'
            message += 'You invited ' + invitee.name + ' to join the timesheet system for ' + invitee.organization.name
            message += '\nYou will receive another email once ' + invitee.name + ' has registered with the site.\n'
            message += 'You can also check the status by going to the onboarding site of the application.\n'
            message += 'Please do not reply to this email.  It will go nowhere'
            send_to = [inviter.user.email]
            reply_tos = []
            mailer.send_and_log_mail(subject, message, sender, send_to, reply_tos,
                                     organization=organization)
            messages.success(request, invitee.name + ' has been invited and emailed.')

        else:
            messages.error(request, 'It looks as if there was an issue inviting this person.  Please check email.')
    organization = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id)).organization
    table = InviteeTable(Invitee.objects.filter(organization=organization).order_by('-status_date'))
    context = {'form': form, 'table': table}
    return render(request, 'tsmanagement/onboarding.html', context)
