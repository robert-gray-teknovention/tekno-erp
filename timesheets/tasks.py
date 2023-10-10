from celery import shared_task
from .utils import TimesheetUtil
from organizations.models import Organization
from datetime import datetime


@shared_task
def check_create_timesheet_period(org_id):
    org = Organization.objects.get(id=org_id)
    util = TimesheetUtil()
    tsp = util.get_timesheet_period(datetime.now(), org)
    print(tsp)
