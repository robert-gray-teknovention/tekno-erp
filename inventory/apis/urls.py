from rest_framework import routers
from django.urls import include, path
from .views import (
    InventoryItemTransactionViewSet,)

router = routers.DefaultRouter()
router.register(r'inventory_item_transactions', InventoryItemTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
    # path('move_or_resize/?', api_move_or_resize_by_code, name='api_move_or_resize_custom')
]
