from django.db import models
from projects.models import Project
from employee.models import TimesheetUser
from timesheets.models import TimesheetEntry

# Create your models here.
class WorkOrder(models.Model):
    class Status(models.Choices):
        CREATED = 'CREATED', 'Created'
        ASSIGNED = 'ASSIGNED', 'Assigned'
        STARTED = 'STARTED', 'Started'
        COMPLETED = 'COMPLETED', 'Completed'
        APPROVED = 'APPROVED', 'Approved'
        CLOSED = 'CLOSED', 'Closed'
        SCRAPPED = 'SCRAPPED', 'Scrapped'


    request = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    assigned_to = models.ManyToManyField(TimesheetUser, related_name='assignees',blank=True)
    creator = models.ForeignKey(TimesheetUser, on_delete=models.SET_NULL, null=True, related_name='creators') 
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)   
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return super().__str__() + f' - {self.request}'

class WorkEntry(TimesheetEntry):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    def __str__(self):
        return f"WorkEntry for WorkOrder {self.work_order.id} - {self.description}" 
