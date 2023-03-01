from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):
    recipients = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Email
        fields = ['id', 'recipients', 'sender', 'subject', 'message', 'date_sent']
