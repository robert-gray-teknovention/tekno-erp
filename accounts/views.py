from django.shortcuts import render, redirect, reverse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.utils import timezone
from timesheets.models import TimesheetEntry, TimesheetPeriod, UserTimesheetPeriod
# from django.core import cache
from employee.models import TimesheetUser, Invitee
from organizations.models import Organization
from datetime import date, datetime
from mailer.utils import Emailer
import pytz
import environ


def register(request):
    if request.method == 'POST':
        env = environ.Env()
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        org_id = request.POST['organization']
        # Check against invitee authentication Code
        invitee = Invitee.objects.filter(authentication_code=request.POST['authentication_code'])
        if len(invitee) < 1:
            message = "I'm sorry but your authorization code is not valid.  Please check your email."
            messages.error(request, message)
            return redirect(reverse('register') + '?org=' + org_id)
        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect(reverse('register') + '?org=' + org_id)
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email id exists')
                    return redirect(reverse('register') + '?org=' + org_id)
                else:
                    # Looks good
                    mailer = Emailer()
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    user.save()
                    tsuser = TimesheetUser()
                    org = Organization.objects.get(id=org_id)
                    tsuser.user = user
                    tsuser.telephone = phone
                    tsuser.hourly_rate = invitee[0].wage
                    tsuser.organization = org
                    tsuser.save()
                    invitee[0].status = Invitee.Status.REGISTERED
                    invitee[0].status_date = datetime.now()
                    invitee[0].save()
                    ts_periods = TimesheetPeriod.objects.filter(org=org).order_by('-date_end')[0:12]
                    for p in ts_periods:
                        utp = UserTimesheetPeriod()
                        utp.period = p
                        utp.user = tsuser
                        print(p.id, ' ', ts_periods.first().id)
                        if p.id != ts_periods.first().id:
                            utp.submitted = True
                            utp.approved = True
                            utp.date_submitted = datetime.now()
                            utp.date_approved = datetime.now()
                        utp.save()
                    # Notify invitee that they are registered
                    subject = 'Welcome ' + invitee[0].name + ' to the ' + invitee[0].organization.name + ' application.'
                    message = 'Dear ' + invitee[0].name + ',\n\n'
                    message += 'You are now registered with the ' + invitee[0].organization.name + ' application\n'
                    message += 'Please go to ' + env('BASE_URL') + 'accounts/login/'
                    message += '\n Thank you for joining our organization.'

                    send_to = [invitee[0].email]
                    reply_tos = []
                    organization = invitee[0].organization
                    sender = organization.mailer_email
                    mailer.send_and_log_mail(subject, message, sender, send_to, reply_tos,
                                             organization=organization)
                    # Notify inviter that the invitee is registered
                    inviter = invitee[0].inviter.user
                    subject = invitee[0].name + ' has registered with the '
                    subject += invitee[0].organization.name + ' application.'
                    message = 'Dear ' + inviter.first_name + ',\n\n'
                    message += invitee[0].name + ' has registered with the ' + invitee[0].organization.name + ' application '
                    message += 'with a wage of ' + str(invitee[0].wage) + ' per hour.\n'
                    message += 'Please do not respond to this email.'
                    send_to = [inviter.email]
                    reply_tos = []
                    organization = invitee[0].organization
                    mailer.send_and_log_mail(subject, message, sender, send_to, reply_tos,
                                             organization=organization)
                    message = 'You are now registered.'
                    messages.success(request, message)
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect(reverse('register') + '?org=' + org_id)
    else:
        org_id = request.GET['org']
        # organizations = Organization.objects.all().order_by('name')
        organization = Organization.objects.get(id=org_id)
        context = {
            'organization': organization,
        }
        return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfully logged out')
        return redirect('index')


def dashboard(request):
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
    user_time_entries = TimesheetEntry.objects.order_by('-date_time_out').filter(period_id=query_period['id'],
                                                                                 user=user)
    user_period = UserTimesheetPeriod.objects.get(user=user, period_id=query_period['id'])
    context = {
        'time_entries': user_time_entries,
        'periods': periods,
        'selected_period': query_period['id'],
        'user_period': user_period
    }

    return render(request, 'accounts/dashboard.html', context)
