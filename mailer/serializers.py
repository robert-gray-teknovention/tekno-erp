from rest_framework import serializers
from .models import Email


class EmailSerializer(serializers.ModelSerializer):
    recipients = serializers.ListField(child=serializers.CharField())
    reply_tos = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Email
        fields = ['id', 'sender', 'recipients', 'subject', 'message', 'date_sent', 'reply_tos', 'organization']
