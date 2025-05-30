from typing import override
from rest_framework import viewsets, generics, status  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response, Serializer  
from rest_framework.permissions import IsAuthenticated  
from django.db.models import Count, Sum, Case, When, Value, IntegerField
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum
from django.core.files.storage import default_storage # type: ignore
from django.core.files.base import ContentFile # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser
import json
import random
from orders.serializers import OrderSerializer
from orders.models import Order
from google.oauth2 import id_token
from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from cloudinary.uploader import upload, destroy
from cloudinary.exceptions import Error as CloudinaryError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.decorators import permission_classes
from api.settings import GOOGLE_CLIENT_ID

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def google_delete(request):
    google_token = request.headers.get('Authorization')

    if not google_token:
        return JsonResponse({'error': 'Google token required'}, status=400)

    try:
        
        id_info = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        user_email = id_info['email']

        user = User.objects.filter(email=user_email).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)

    except ValueError:
        return JsonResponse({'error': 'Invalid Google token'}, status=400)




#google auth
@api_view(['POST'])
def google_auth(request):
    token = request.data.get('token')

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo['email']
        username = email.split('@')[0]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': username}
        )

        if created:
            user.set_unusable_password()
            user.save()

        auth_token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'status': 'success',
            'token': auth_token.key,
            'user_id': user.id,
            'email': user.email,
            'username': user.username 
        })

    except ValueError:
        return Response({'status': 'invalid token'}, status=400)


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

class HomeBrandList(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer

    def get_queryset(self):
        queryset = list(models.Brand.objects.all())
        random.shuffle(queryset)
        return queryset[:30]


class BrandList(generics.ListAPIView):
    """API view that lists all product brands."""
    serializer_class = serializers.BrandSerializer  
    queryset = models.Brand.objects.all()
    permission_classes = [AllowAny]



class BrandDetails(generics.RetrieveAPIView):
    """API view that retrieves brand details for the authenticated user."""
    serializer_class = serializers.BrandSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return models.Brand.objects.get(owner=self.request.user)

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

    def update(self, request, *args, **kwargs):
        """Update an existing product instance."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            
            queryset = queryset.filter(brand__icontains=search_query)  
        return queryset


class ProductsByBrand(generics.ListAPIView):
    """API view that lists products filtered by brand with optional search."""
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        """Filter products by brand ID and optional search query in title."""
        brand_id = self.kwargs.get("brand_id")
        search_query = self.request.query_params.get("search", None) 

        queryset = models.Product.objects.filter(brand_id=brand_id)  

        if search_query:
            queryset = queryset.filter(title__icontains=search_query) 

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
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        
        # Prevent duplicate registration
        if models.DeliveryBoy.objects.filter(user=user).exists():
            return Response({"error": "You are already registered as a delivery boy."},
                            status=status.HTTP_400_BAD_REQUEST)
                            
        
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        # Save with the user from the token
        serializer.save(user=user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
            return models.Brand.objects.filter(title__icontains=query)  
        return models.Brand.objects.none()

class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD operations on brands."""
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Prevent user from creating multiple brands
        if models.Brand.objects.filter(owner=request.user).exists():
            return Response({"error": "Brand already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

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

#Create or update product
class CreateOrUpdateProductView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        brand = request.user.brands.first()
        if not brand:
            return Response({"error": "No brand associated with this user."}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data.get('product_id')
        is_update = bool(product_id)
        product = None

        if is_update:
            try:
                product = models.Product.objects.get(id=product_id, brand=brand)
            except models.Product.DoesNotExist:
                return Response({"error": "Product not found or not owned by this brand."}, status=status.HTTP_404_NOT_FOUND)

        new_images = request.FILES.getlist('images')
        image_urls = []
        image_public_ids = []

        # Delete old Cloudinary images if updating and new ones are provided
        if is_update and new_images:
            if product.imagePublicIds:
                for public_id in product.imagePublicIds:
                    try:
                        destroy(public_id)
                    except Exception:
                        pass  # You can log this

        # Upload new images
        if new_images:
            for image in new_images:
                if not image.name.lower().endswith(('png', 'jpg', 'jpeg')):
                    return Response({"error": f"{image.name} must be PNG, JPG or JPEG"}, status=status.HTTP_400_BAD_REQUEST)
                if image.size > 5 * 1024 * 1024:
                    return Response({"error": f"{image.name} exceeds 5MB"}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    result = upload(image)
                    image_urls.append(result['secure_url'])
                    image_public_ids.append(result['public_id'])
                except CloudinaryError as e:
                    return Response({"error": f"Upload failed for {image.name}: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        elif is_update:
            image_urls = product.imageUrls or []
            image_public_ids = product.imagePublicIds or []

        if not is_update and not image_urls:
            return Response({"error": "At least one product image is required."}, status=status.HTTP_400_BAD_REQUEST)

        def parse_json_field(field):
            value = request.data.get(field)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return Response({"error": f"Invalid JSON in '{field}'"}, status=status.HTTP_400_BAD_REQUEST)
            return None

        try:
            if is_update:
                fields = ['title', 'description', 'price', 'rating', 'stock', 'is_featured', 'category']
                for field in fields:
                    if field in request.data:
                        if field == 'is_featured':
                            product.is_featured = request.data.get(field) in ['true', 'True', True]
                        elif field == 'category':
                            product.category_id = request.data.get('category')
                        else:
                            setattr(product, field, request.data.get(field))

                if new_images:
                    product.imageUrls = image_urls
                    product.imagePublicIds = image_public_ids

                for json_field in ['addons', 'ingredients', 'dietary_restrictions']:
                    if json_field in request.data:
                        parsed = parse_json_field(json_field)
                        if isinstance(parsed, Response):
                            return parsed
                        setattr(product, json_field, parsed)

                product.save()
                return Response(serializers.ProductSerializer(product).data, status=status.HTTP_200_OK)

            else:
                new_product = models.Product.objects.create(
                    brand=brand,
                    title=request.data.get('title'),
                    description=request.data.get('description'),
                    price=request.data.get('price'),
                    imageUrls=image_urls,
                    imagePublicIds=image_public_ids,
                    rating=request.data.get('rating') or 0,
                    stock=request.data.get('stock') or 0,
                    is_featured=request.data.get('is_featured') in ['true', 'True', True],
                    addons=parse_json_field('addons'),
                    ingredients=parse_json_field('ingredients'),
                    dietary_restrictions=parse_json_field('dietary_restrictions'),
                    category_id=request.data.get('category'),
                )
                return Response(serializers.ProductSerializer(new_product).data, status=status.HTTP_201_CREATED)

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
        week_ago = today - timedelta(days=7)
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