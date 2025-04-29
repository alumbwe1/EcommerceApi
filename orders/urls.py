from django.urls import path
from .views import (
    OrderStats, 
    CreateOrderView, 
    UpdateOrderStatusView,
    OrderDetailView,
    CustomerOrdersView,
    DeliveryBoyStatusView
)

urlpatterns = [
    # URL for creating an order
    path('create/', CreateOrderView.as_view(), name='create-order'), 
    # URL for getting order statistics
    path('stats/', OrderStats.as_view(), name='order-stats'),  
    # Order management
    path('<int:order_id>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('my-orders/', CustomerOrdersView.as_view(), name='customer-orders'),
    path('personel-status/<int:delivery_boy_id>/', DeliveryBoyStatusView.as_view(), name='delivery-boy-status'),
]
