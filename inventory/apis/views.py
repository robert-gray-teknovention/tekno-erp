from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from inventory.models import InventoryItemTransaction
from .serializers import InventoryItemTransactionSerializer

class InventoryItemTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryItemTransaction.objects.all().order_by('-timestamp')
    search_fields = ['item', 'location', 'transaction_type']
    serializer_class = InventoryItemTransactionSerializer  # You would need to define a serializer for this model
    # override get_queryset to allow filtering based item_id and location_id query params
    def get_queryset(self):
        queryset = super().get_queryset()
        item_id = self.request.query_params.get('item_id', None)
        location_id = self.request.query_params.get('location_id', None)
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)
        if location_id is not None:
            queryset = queryset.filter(location_id=location_id)
        return queryset