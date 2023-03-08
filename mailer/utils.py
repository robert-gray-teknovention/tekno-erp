from .models import Email
from django.core.mail import EmailMessage
from employee.models import TimesheetUser
from timesheets.models import UserTimesheetPeriod


def email_unsubmitted(org, period):
    users = TimeSheetUser.objects.filter(org=org)
    for u in users:
        utp = UserTimesheetPeriod.objects.get(user=u, period=period)
        if not utp.submitted:
            recipients = [org.mailer_emai]
