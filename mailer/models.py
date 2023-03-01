from django.db import models
from django.contrib.postgres.fields import ArrayField


class Email(models.Model):
    sender = models.EmailField(max_length=75)
    recipients = ArrayField(
        ArrayField(
            models.EmailField(max_length=75),
            size=50,
            ),
        size=50,
    )
    subject = models.CharField(max_length=250)
    message = models.CharField(max_length=2500)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient
