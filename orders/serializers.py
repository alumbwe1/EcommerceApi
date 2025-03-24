from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, source='orderitem_set')  # Nested serializer for order items

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'brand', 'order_items', 'total_price', 
            'payment_method', 'delivery_type', 'delivery_location', 
            'room_number', 'address', 'is_paid', 'is_delivered', 
            'delivery_time', 'created_at', 'updated_at', 
            'delivery_boy', 'order_status'
        ]
