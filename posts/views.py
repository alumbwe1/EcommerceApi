from rest_framework import viewsets, generics, status  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated  
from django.db.models import Count  
from django.utils import timezone
from django.db.models import Count, Sum
from django.core.files.storage import default_storage # type: ignore
from django.core.files.base import ContentFile # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser
import json

import random
from orders.serializers import OrderSerializer
from orders.models import Order

from . import models, serializers


class CategoryList(generics.ListAPIView):
    """API view that lists all product categories."""
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class HomeCategoryList(generics.ListAPIView):
    """API view that returns 5 randomly selected categories for the home page."""
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = list(models.Category.objects.all())
        random.shuffle(queryset)
        return queryset[:5]


class BrandList(generics.ListAPIView):
    """API view that lists all product brands."""
    serializer_class = serializers.BrandSerializer  
    queryset = models.Brand.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on products."""
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        """Return different serializers based on the action being performed."""
        if self.action in ["create", "update"]:
            return serializers.ProductCreateSerializer  
        return serializers.ProductSerializer  

    def perform_create(self, serializer):
        """Save the new product instance."""
        serializer.save()


class ProductList(generics.ListAPIView):
    """API view that returns 20 randomly selected products."""
    serializer_class = serializers.ProductSerializer  

    def get_queryset(self):
        queryset = list(models.Product.objects.all())
        random.shuffle(queryset)
        return queryset[:20]


class PopularProductList(generics.ListAPIView):
    """API view that returns 5 randomly selected products (simulating popular products)."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = list(models.Product.objects.all())
        random.shuffle(queryset)
        return queryset[:5]


class SearchProduct(generics.ListAPIView):
    """API view for searching products by title."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Filter products based on search query in the title."""
        query = self.request.query_params.get("q", None)
        if query:
            return models.Product.objects.filter(title__icontains=query)  
        return models.Product.objects.none()


class ProductsByCategory(generics.ListAPIView):
    """API view that lists products filtered by category."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Filter products by the category ID from URL parameter."""
        category_id = self.kwargs.get("category_id")
        if category_id:
            return models.Product.objects.filter(category_id=category_id)
        return models.Product.objects.none()

class SearchProductByBrand(generics.ListAPIView):
    """API view for searching products within a specific brand."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Filter products by brand ID and optional search query."""
        brand_id = self.kwargs.get("brand_id")
        search_query = self.request.query_params.get("q", None)
        queryset = models.Product.objects.filter(brand_id=brand_id)

        if search_query:
            # NOTE: This may be incorrect - 'brand__icontains' should likely be 'title__icontains'
            queryset = queryset.filter(brand__icontains=search_query)  # Corrected lookup
        return queryset


class ProductsByBrand(generics.ListAPIView):
    """API view that lists products filtered by brand with optional search."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Filter products by brand ID and optional search query in title."""
        brand_id = self.kwargs.get("brand_id")
        search_query = self.request.query_params.get("search", None)  # Get the search query from the request

        queryset = models.Product.objects.filter(brand_id=brand_id)  # Filter products by brand

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)  # Filter products by search query in title

        return queryset

class SimilarProducts(generics.ListAPIView):
    """API view that returns similar products based on category."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Return up to 5 products from the same category as the given product."""
        product_id = self.kwargs.get("product_id")
        try:
            product = models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            return models.Product.objects.none()

        # Fetch products from the same category, excluding the current product
        return models.Product.objects.filter(category=product.category).exclude(id=product_id)[:5]


class DeliveryBoyViewSet(viewsets.ModelViewSet):
    """ViewSet for handling delivery boy operations."""
    
    queryset = models.DeliveryBoy.objects.all()
    serializer_class = serializers.DeliveryBoySerializer


class CategoriesByBrand(generics.ListAPIView):
    """API view that lists categories associated with a specific brand."""
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        """Filter categories by brand ID."""
        brand_id = self.kwargs.get("brand_id")
        if brand_id:
            return models.Category.objects.filter(brands__id=brand_id)  
        return models.Category.objects.none()


class ProductsByCategoryAndBrand(generics.ListAPIView):
    """API view that lists products filtered by both category and brand."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Filter products by both category ID and brand ID."""
        category_id = self.kwargs.get("category_id")
        brand_id = self.kwargs.get("brand_id")
        if category_id and brand_id:
            return models.Product.objects.filter(category_id=category_id, brand_id=brand_id)
        return models.Product.objects.none()

class BrandsByCategory(generics.ListAPIView):
    """API view that lists brands associated with a specific category."""
    serializer_class = serializers.BrandSerializer

    def get_queryset(self):
        """Filter brands by category ID."""
        category_id = self.kwargs.get("category_id")
        if category_id:
            return models.Brand.objects.filter(categories__id=category_id)  
        return models.Brand.objects.none()

class SearchBrand(generics.ListAPIView):
    """API view for searching brands."""
    serializer_class = serializers.BrandSerializer

    def get_queryset(self):
        """Filter brands based on search query."""
        query = self.request.query_params.get("q", None)
        if query:
            # ERROR: Missing field name before __icontains
            # Should be something like: models.Brand.objects.filter(name__icontains=query)
            return models.Brand.objects.filter(__icontains=query)  
        return models.Brand.objects.none()

class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on brands."""
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the new brand and associate it with the current user."""
        serializer.save(owner=self.request.user) 

    def get_queryset(self):
        """Return all brands."""
        return models.Brand.objects.all()  
    

class DeleveryViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on delivery boys
    """
    queryset = models.DeliveryBoy.objects.all()
    serializer_class = serializers.DeliveryBoySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the new delivery boy and associate it with the current user
        """
        return serializer.save(user=self.request.user)
    

class DashboardStats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_brands = models.Brand.objects.filter(owner=user)

        total_products = models.Product.objects.filter(brand__in=user_brands).count()

        products_per_brand = user_brands.annotate(
            product_count=Count('products')
        ).aggregate(total=Sum('product_count'))['total'] or 0

        categories_per_brand = user_brands.annotate(
            category_count=Count('categories')
        ).aggregate(total=Sum('category_count'))['total'] or 0

        return Response({
            "total_products": total_products,
            "products_per_brand": products_per_brand,
            "categories_per_brand": categories_per_brand,
        })
class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        brand = request.user.brands.first()
        if not brand:
            return Response({"error": "No brand associated with this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Handle image uploads
        image_urls = []
        if request.FILES.getlist('images'):
            for image in request.FILES.getlist('images'):
                if not image.name.lower().endswith(('png', 'jpg', 'jpeg')):
                    return Response({"error": "Invalid image format - only PNG/JPG/JPEG allowed"}, status=status.HTTP_400_BAD_REQUEST)
                if image.size > 5 * 1024 * 1024:
                    return Response({"error": f"{image.name} exceeds 5MB size limit"}, status=status.HTTP_400_BAD_REQUEST)

                path = default_storage.save(f'products/{brand.id}/{image.name}', ContentFile(image.read()))
                image_urls.append(default_storage.url(path))

        if not image_urls:
            return Response({"error": "At least one product image is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Parse JSON fields if needed
        def parse_json_field(field):
            value = request.data.get(field)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return None
            return None

        # Create product
        try:
            product = models.Product.objects.create(
                brand=brand,
                title=request.data.get('title'),
                description=request.data.get('description'),
                price=request.data.get('price'),
                imageUrls=image_urls,
                rating=request.data.get('rating') or 0,
                stock=request.data.get('stock') or 0,
                is_featured=request.data.get('is_featured') in ['true', 'True', True],
                addons=parse_json_field('addons'),
                category_id=request.data.get('category'),
                ingredients=parse_json_field('ingredients'),
                dietary_restrictions=parse_json_field('dietary_restrictions'),
            )

            return Response(serializers.ProductSerializer(product).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryBoyEarnings(APIView):
    """API view for delivery boy earnings statistics."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            delivery_boy = models.DeliveryBoy.objects.get(user=request.user)
        except models.DeliveryBoy.DoesNotExist:
            return Response({"error": "No DeliveryBoy found for this user"}, status=404)

        today = timezone.now().date()
        
        # Daily earnings
        daily_stats = Order.objects.filter(
            delivery_boy=delivery_boy,
            order_status='delivered',
            created_at__date=today
        ).aggregate(
            total_orders=Count('id'),
            total_earnings=Sum('total_price')
        )

        # Weekly earnings (last 7 days)
        week_ago = today - timezone.timedelta(days=7)
        weekly_stats = Order.objects.filter(
            delivery_boy=delivery_boy,
            order_status='delivered',
            created_at__date__gte=week_ago
        ).aggregate(
            total_orders=Count('id'),
            total_earnings=Sum('total_price')
        )

        # Monthly earnings
        month_start = today.replace(day=1)
        monthly_stats = Order.objects.filter(
            delivery_boy=delivery_boy,
            order_status='delivered',
            created_at__date__gte=month_start
        ).aggregate(
            total_orders=Count('id'),
            total_earnings=Sum('total_price')
        )

        return Response({
            'daily': {
                'orders': daily_stats['total_orders'] or 0,
                'earnings': float(daily_stats['total_earnings'] or 0)
            },
            'weekly': {
                'orders': weekly_stats['total_orders'] or 0,
                'earnings': float(weekly_stats['total_earnings'] or 0)
            },
            'monthly': {
                'orders': monthly_stats['total_orders'] or 0,
                'earnings': float(monthly_stats['total_earnings'] or 0)
            }
        })



class DeliveryBoyOrders(generics.ListAPIView):
    """API view for delivery boy's orders."""
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        delivery_boy = models.DeliveryBoy.objects.get(user=self.request.user)
        status = self.request.query_params.get('status', None)
        
        queryset = Order.objects.filter(delivery_boy=delivery_boy)
        
        if status:
            queryset = queryset.filter(order_status=status)
            
        return queryset.order_by('-created_at')

class DeliveryBoyOrderSummary(APIView):
    """API view for delivery boy's order summary."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        delivery_boy = models.DeliveryBoy.objects.get(user=request.user)
        
        # Get summary of orders by status
        status_summary = Order.objects.filter(
            delivery_boy=delivery_boy
        ).values('order_status').annotate(
            count=Count('id')
        )
        
        # Calculate average delivery time for completed orders
        completed_orders = Order.objects.filter(
            delivery_boy=delivery_boy,
            order_status='delivered'
        )
        
        total_delivery_time = timezone.timedelta()
        completed_count = completed_orders.count()
        
        for order in completed_orders:
            if order.delivery_time:
                delivery_time = order.delivery_time - order.created_at
                total_delivery_time += delivery_time
        
        avg_delivery_time = (total_delivery_time / completed_count).total_seconds() / 60 if completed_count > 0 else 0
        
        return Response({
            'status_summary': status_summary,
            'total_orders': Order.objects.filter(delivery_boy=delivery_boy).count(),
            'completed_orders': completed_count,
            'average_delivery_time_minutes': round(avg_delivery_time, 2)
        })