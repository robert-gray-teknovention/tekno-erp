from celery import shared_task
from employee.models import TimesheetUser
from timesheets.models import UserTimesheetPeriod
from mailer.utils import Emailer
from timesheets.utils import TimesheetUtil
from datetime import datetime
from organizations.models import Organization
import pytz


@shared_task
def saying_hello(**kwargs):
    additional = kwargs['additional']
    main = kwargs['main']
    print(main)
    print(additional)
    mailer = Emailer()
    org = Organization.objects.get(name='Teknovention')
    mailer.send_and_log_mail('Tester from me', 'This is merely a test', 'mailer@mail.teknovention.com',
                             ['jjohannson@hotmail.com'], ['rgray@teknovention'], organization=org)


@shared_task
def email_unsubmitted(org_id):
    org = Organization.objects.get(id=org_id)
    tsutil = TimesheetUtil()
    period = tsutil.get_timesheet_period(datetime.now(pytz.timezone(org.timezone)), org)
    users = TimesheetUser.objects.filter(organization_id=org)
    reply_tos = []
    for u in users:
        if u.user.is_active:
            utps = UserTimesheetPeriod.objects.filter(user=u, period=period)
            if utps.count() > 0:
                if not utps[0].submitted:
                    subject = 'Your timesheet for the period ' + str(utps[0]) + ' has not been submitted'
                    message = 'Dear ' + u.user.first_name + ',\n\tYour timesheet is due for ' + org.name + '.\nPlease reply to this message after it is submitted.'
                    sender = org.mailer_email
                    for a in u.approvers.all():
                        reply_tos.append(a.user.email)
                    recipients = [u.user.email]
                    mailer = Emailer()
                    mailer.send_and_log_mail(subject, message, sender, recipients, reply_tos, organization=org)
