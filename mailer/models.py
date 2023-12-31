from django.db import models
from django.contrib.postgres.fields import ArrayField
from organizations.models import Organization


class Email(models.Model):
    sender = models.EmailField(max_length=75)
    recipients = ArrayField(
        ArrayField(
            models.EmailField(max_length=75),
            size=50,
            ),
        size=50,
    )
    reply_tos = ArrayField(
        ArrayField(
            models.EmailField(max_length=75),
            size=50,
            ),
        size=50, null=True,
    )
    subject = models.CharField(max_length=250)
    message = models.CharField(max_length=2500)
    date_sent = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.recipients)
