from django import forms
from django.contrib.postgres.forms import SimpleArrayField


class MailForm(forms.Form):
    recipients = SimpleArrayField(forms.EmailField(max_length=200))
    reply_tos = SimpleArrayField(forms.EmailField(max_length=200))
    subject = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}))
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}))
