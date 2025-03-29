from django.utils import timezone
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, DeliveryBoy
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework import status

class OrderStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()

        # Calculate the number of orders by status
        completed_orders_count = Order.objects.filter(order_status='delivered').count()
        cancelled_orders_count = Order.objects.filter(order_status='cancelled').count()
        pending_orders_count = Order.objects.filter(order_status='pending').count()

        # Calculate total sales amount
        total_sales = Order.objects.filter(order_status='delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Calculate the number of orders for a day
        today_orders_count = Order.objects.filter(created_at__date=today).count()

        return Response({
            "completed_orders": completed_orders_count,
            "cancelled_orders": cancelled_orders_count,
            "pending_orders": pending_orders_count,
            "total_sales": total_sales,
            "today_orders": today_orders_count,
        })

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validate order items
        if not request.data.get('order_items'):
            return Response(
                {"error": "order_items is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total price
        total_price = sum(
            float(item['price']) * int(item['quantity'])
            for item in request.data.get('order_items', [])
        )

    
        delivery_boy = Order.objects.filter(order_status='delivered').values('delivery_boy_id').annotate(count=Count('id')).order_by('count').first()
        delivery_boy_id = delivery_boy['delivery_boy_id'] if delivery_boy else None

        # Prepare order data
        order_data = {
            'brand_id': request.data.get('brand_id'),
            'total_price': total_price,
            'payment_method': request.data.get('payment_method'),
            'delivery_type': request.data.get('delivery_type'),
            'delivery_location': request.data.get('delivery_location'),
            'room_number': request.data.get('room_number'),
            'address': request.data.get('address'),
            'order_status': 'pending',
            'customer': request.user.id,
            'delivery_boy_id': delivery_boy_id 
        }

        # Create order with items
        serializer = OrderSerializer(
            data=order_data,
            context={
                'request': request,
                'order_items': request.data.get('order_items', [])
            }
        )

        if serializer.is_valid():
            order = serializer.save()
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            new_status = request.data.get('status')
            
            if new_status not in dict(Order.ORDER_STATUS_CHOICES):
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            
            order.order_status = new_status
            if new_status == 'delivered':
                order.delivery_time = timezone.now()
                order.is_delivered = True
            order.save()
            
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class CustomerOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class DeliveryBoyStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, delivery_boy_id):
        # Assuming there's a field `is_online` in the DeliveryBoy model
        try:
            delivery_boy = DeliveryBoy.objects.get(id=delivery_boy_id)
            return Response({"is_online": delivery_boy.is_online})
        except DeliveryBoy.DoesNotExist:
            return Response({"error": "Delivery boy not found"}, status=status.HTTP_404_NOT_FOUND)