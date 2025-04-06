
from django.db import models
from django.utils import timezone
from posts.models import Product, Brand,DeliveryBoy
from django.contrib.auth.models import User
class Order(models.Model):
    DELIVERY_TYPE_CHOICES = [
        ('instant', 'Instant Delivery'),
        ('scheduled', 'Scheduled Delivery'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Card Payment'),
    ]

    DELIVERY_LOCATION_CHOICES = [
        ('on_campus', 'On Campus'),
        ('off_campus', 'Off Campus'),
    ]

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),               # Order placed, waiting for confirmation
        ('accepted', 'Accepted'),             # Restaurant/brand accepted the order
        ('preparing', 'Preparing'),           # Order being prepared
        ('on the way', 'On The way'),  # Assigned delivery boy, on the way
        ('delivered', 'Delivered'),           # Successfully delivered
        ('cancelled', 'Cancelled'),           # Order cancelled
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES)
    delivery_location = models.CharField(max_length=20, choices=DELIVERY_LOCATION_CHOICES)
    room_number = models.CharField(max_length=50, blank=True, null=True)  # For campus
    address = models.TextField(blank=True, null=True)  # For off-campus
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    delivery_time = models.DateTimeField(null=True, blank=True)  # For scheduled delivery
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # ✅ New field: order status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.customer.username} - {self.order_status}"


# For connecting Products to Order with quantity
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order {self.order.id}"
