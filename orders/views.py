from django.utils import timezone
from django.db.models import Count, Sum, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer
from posts.models import DeliveryBoy, Brand
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

class OrderStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_brands = Brand.objects.filter(owner=user)
        brand_orders = Order.objects.filter(brand__in=user_brands)
        today = timezone.now().date()
        start_of_week = today - timezone.timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        # Calculates the number of orders by status
        completed_orders_count = brand_orders.filter(order_status='delivered').count()
        cancelled_orders_count = brand_orders.filter(order_status='cancelled').count()
        pending_orders_count = brand_orders.filter(order_status='pending').count()
        
        # Calculates total sales amount
        total_sales = brand_orders.filter(order_status='delivered').aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Calculates sales for different time periods
        today_sales = brand_orders.filter(order_status='delivered', created_at__date=today).aggregate(Sum('total_price'))['total_price__sum'] or 0

        weekly_sales = brand_orders.filter(order_status='delivered', created_at__date__gte=start_of_week, created_at__date__lte=today).aggregate(Sum('total_price'))['total_price__sum'] or 0

        monthly_sales = brand_orders.filter(order_status='delivered', created_at__date__gte=start_of_month, created_at__date__lte=today).aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Calculates the number of orders for a day
        today_orders_count = brand_orders.filter(created_at__date=today).count()

        return Response({
            "completed_orders": completed_orders_count,
            "cancelled_orders": cancelled_orders_count,
            "pending_orders": pending_orders_count,
            "total_sales": total_sales,
            "today_orders": today_orders_count,
            "today_sales": today_sales,
            "weekly_sales": weekly_sales,
            "monthly_sales": monthly_sales,
        })

class CreateOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Validates order items FIRST
        order_items = request.data.get('order_items', [])
        if not isinstance(order_items, list) or len(order_items) == 0:
            return Response(
                {"order_items": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process the request data directly
        request.data['customer'] = request.user.id

        # Find the online delivery boy with the least number of completed deliveries
        delivery_boy = DeliveryBoy.objects.filter(
            is_online=True
        ).annotate(
            completed_deliveries=Count('orders', filter=Q(orders__order_status='delivered'))
        ).order_by('completed_deliveries').first()

        if delivery_boy is None:
            return Response(
                {"error": "No online delivery boys available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Assigns the selected delivery boy to the order data
        request.data['delivery_boy_id'] = delivery_boy.id
        # Creates the order
        serializer = OrderSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            order = serializer.save()
        
        
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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


class BrandOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, brand_id):
        orders = Order.objects.filter(brand_id=brand_id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


#Online Status view for a delievery personal
class DeliveryBoyStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, delivery_boy_id):
        try:
            delivery_boy = DeliveryBoy.objects.get(user__id=delivery_boy_id)
            return Response({"is_online": delivery_boy.is_online}, status=status.HTTP_200_OK)
        except DeliveryBoy.DoesNotExist:
            return Response({"error": "Delivery boy not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, delivery_boy_id):
        try:
            delivery_boy = DeliveryBoy.objects.get(user__id=delivery_boy_id)
        except DeliveryBoy.DoesNotExist:
            return Response({"error": "Delivery boy not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if request.user.id != delivery_boy.user.id:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

        is_online = request.data.get('is_online')
        if not isinstance(is_online, bool):
            return Response({"error": "'is_online' must be a boolean"}, status=status.HTTP_400_BAD_REQUEST)

        delivery_boy.is_online = is_online
        delivery_boy.save()

        return Response({
            "message": "Status updated successfully",
            "is_online": delivery_boy.is_online
        }, status=status.HTTP_200_OK)