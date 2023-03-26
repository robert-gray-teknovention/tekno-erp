from celery import shared_task
from .utils import TimesheetUtil
from organizations.models import Organization
from datetime import datetime


@shared_task
def check_create_timesheet_period():
    orgs = Organization.objects.all()
    for org in orgs:
        util = TimesheetUtil()
        tsp = util.get_timesheet_period(datetime.now(), org)
        print(tsp)
