from django.shortcuts import render
from django.http import JsonResponse
from .serializers import EmailSerializer
from django.core.mail import send_mail
import json


def email(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('email'))
        # data = json.loads(request.POST.get('email'))
        serializer = EmailSerializer(data=data)
        if serializer.is_valid():
            # Send email
            print(data['sender'])
            send_mail(data['subject'], data['message'], 'john@john.com', data['recipients'], fail_silently='False')
            serializer.save()
            return JsonResponse({"message": "Email send and saved"})
        else:
            return JsonResponse(status=404, data={'status': 'false', 'message': 'Email failed'})
    return render(request, 'tsmanagement/managedashboard.html')
