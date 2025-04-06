from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, OrderItem
from posts.models import Product, Brand, DeliveryBoy

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'description', 'image', 'phone', 'email', 'rating']

class DeliveryBoySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DeliveryBoy
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'imageUrls', 'brand']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    
    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity', 'price']
        extra_kwargs = {
            'quantity': {'min_value': 1},
            'price': {'min_value': 0}
        }

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(
        many=True,
        required=True,
        write_only=True
    )
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        write_only=True,
        source='brand'
    )
    delivery_boy = DeliveryBoySerializer(read_only=True)
    delivery_boy_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryBoy.objects.all(),
        write_only=True,
        source='delivery_boy'
    )

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'brand', 'brand_id', 'order_items',
            'total_price', 'payment_method', 'delivery_type',
            'delivery_location', 'room_number', 'address',
            'order_status', 'delivery_boy', 'delivery_boy_id', 'created_at'
        ]
        read_only_fields = ['created_at']

    def create(self, validated_data):
        # Extract order items FIRST
        order_items_data = validated_data.pop('order_items')
        
        # Create the order
        order = Order.objects.create(**validated_data)
        
        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order

    def to_representation(self, instance):
        """Show order items in response"""
        rep = super().to_representation(instance)
        rep['order_items'] = OrderItemSerializer(
            instance.orderitem_set.all(),
            many=True
        ).data
        return rep