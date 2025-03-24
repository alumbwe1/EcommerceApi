from django.utils import timezone
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from .serializers import OrderSerializer
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
        # Deserialize the request data
        serializer = OrderSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the order
            order = serializer.save(customer=request.user)  
            
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)