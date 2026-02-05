from rest_framework import serializers
from inventory.models import InventoryItemTransaction

class InventoryItemTransactionSerializer(serializers.ModelSerializer):
    notes = serializers.CharField(read_only=True)
    class Meta:
        model = InventoryItemTransaction
        fields = ('__all__')