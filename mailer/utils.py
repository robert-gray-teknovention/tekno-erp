from .models import Email
from django.core.mail import EmailMessage


class Emailer:
    def send_and_log_mail(self, subject, message, sender, recipients, reply_tos, **kwargs):
        log_email = Email()
        log_email.subject = subject
        log_email.message = message
        log_email.sender = sender
        log_email.recipients = recipients
        log_email.reply_tos = reply_tos
        log_email.organization = kwargs['organization']
        email = EmailMessage(subject, message, sender, to=recipients, reply_to=reply_tos)
        email.send()
        log_email.save()
