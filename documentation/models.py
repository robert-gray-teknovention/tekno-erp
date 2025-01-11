from django.db import models
from purchasing.models import Item
from timesheets.models import TimesheetEntry


class Documentation(models.Model):
    file = models.FileField(upload_to="documentation/")
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.file} {self.description}"

    class Meta:
        abstract = True


class ItemDocumentation(Documentation):
    parent = models.ForeignKey(Item, on_delete=models.CASCADE)


class TimesheetEntryDocumentation(Documentation):
    parent = models.ForeignKey(TimesheetEntry, on_delete=models.CASCADE)
