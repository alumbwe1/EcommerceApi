from rest_framework import serializers
from .models import Order, OrderItem
from django.contrib.auth.models import User
from posts.models import Product, Brand, DeliveryBoy
from posts.serializers import ProductSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'description', 'image', 'phone', 'email', 'rating']

class DeliveryBoySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = DeliveryBoy
        fields = ['id', 'user', 'name', 'phone_number', 'profile_pic', 'vehicle_type']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, source='orderitem_set')
    customer = UserSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    delivery_boy = DeliveryBoySerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        write_only=True,
        source='brand'
    )
    delivery_boy_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryBoy.objects.all(),
        write_only=True,
        source='delivery_boy',
        required=False,
        allow_null=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'brand', 'brand_id', 'order_items',
            'total_price', 'payment_method', 'delivery_type',
            'delivery_location', 'room_number', 'address',
            'is_paid', 'is_delivered', 'delivery_time',
            'created_at', 'updated_at', 'delivery_boy',
            'delivery_boy_id', 'order_status'
        ]
        read_only_fields = ['customer', 'is_delivered', 'delivery_time']

    def create(self, validated_data):
        order_items_data = self.context.get('order_items', [])
        order = Order.objects.create(
            customer=self.context['request'].user,
            brand=validated_data['brand'],
            total_price=validated_data['total_price'],
            payment_method=validated_data['payment_method'],
            delivery_type=validated_data['delivery_type'],
            delivery_location=validated_data['delivery_location'],
            room_number=validated_data.get('room_number'),
            address=validated_data.get('address'),
            delivery_boy=validated_data.get('delivery_boy'),
            order_status=validated_data.get('order_status', 'pending')
        )

        # Create order items
        for item_data in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )

        return order
