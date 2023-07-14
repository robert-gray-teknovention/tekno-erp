from django import forms
from employee.models import Invitee


class InviteeForm(forms.ModelForm):
    class Meta:
        model = Invitee
        fields = ['name', 'email', 'wage']
