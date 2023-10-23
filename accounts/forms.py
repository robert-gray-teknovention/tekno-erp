from django import forms
from django.contrib.auth.forms import SetPasswordForm


class RecoverUserForm(forms.Form):
    email = forms.EmailField(max_length=100)


class ResetPasswordForm(SetPasswordForm):
    code = forms.CharField(max_length=10)
    user_id = forms.IntegerField()
