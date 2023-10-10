from django.shortcuts import render
from django.http import JsonResponse
from .serializers import EmailSerializer
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from employee.models import TimesheetUser
import re
import json


def email(request):
    if request.method == 'POST':
        ts_user = TimesheetUser.objects.get(user=User.objects.get(id=request.user.id))
        data = json.loads(request.POST.get('email'))
        data['organization'] = ts_user.organization.id
        serializer = EmailSerializer(data=data)
        if serializer.is_valid():
            # Send email
            recipients = re.split(r'[,;]', data['recipients'][0].replace(' ', ''))
            reply_tos = re.split(r'[,;]', data['reply_tos'][0].replace(' ', ''))
            # for r in recipients:
            email = EmailMessage(data['subject'], data['message'], data['sender'], to=recipients,
                                 reply_to=reply_tos)
            # email = EmailMessage(data['subject'], data['message'], to=recipients)
            email.send()
            serializer.save()
            return JsonResponse({"message": "Email sent and saved"})
        else:
            print(serializer.errors)
            return JsonResponse(status=404, data={'status': 'false', 'message': 'Email failed'})
    return render(request, 'tsmanagement/managedashboard.html')
