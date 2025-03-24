from django.urls import path
from .views import OrderStats, CreateOrderView

urlpatterns = [
    # URL for creating an order
    path('create/', CreateOrderView.as_view(), name='create-order'), 
    # URL for getting order statistics
    path('stats/', OrderStats.as_view(), name='order-stats'),  
]
