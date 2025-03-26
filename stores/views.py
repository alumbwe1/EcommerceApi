from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Avg
from django.utils import timezone
from .models import StoreCategory, Store, StoreProduct, StoreReview
from .serializers import (
    StoreCategorySerializer,
    StoreSerializer,
    StoreListSerializer,
    StoreProductSerializer,
    StoreReviewSerializer
)

# Create your views here.

class StoreCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for store categories."""
    queryset = StoreCategory.objects.filter(is_active=True)
    serializer_class = StoreCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StoreViewSet(viewsets.ModelViewSet):
    """ViewSet for stores."""
    queryset = Store.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return StoreListSerializer
        return StoreSerializer

    def get_queryset(self):
        queryset = Store.objects.all()
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by featured
        featured = self.request.query_params.get('featured', None)
        if featured:
            queryset = queryset.filter(is_featured=True)
            
        return queryset

class StoreProductViewSet(viewsets.ModelViewSet):
    """ViewSet for store products."""
    serializer_class = StoreProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        return StoreProduct.objects.filter(store_id=store_id)

class StoreReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for store reviews."""
    serializer_class = StoreReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        return StoreReview.objects.filter(store_id=store_id)

class MyStoresView(generics.ListAPIView):
    """View for listing stores owned by the current user."""
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(owner=self.request.user)

class FeaturedStoresView(generics.ListAPIView):
    """View for listing featured stores."""
    serializer_class = StoreListSerializer
    queryset = Store.objects.filter(is_featured=True, status='active')

class SearchStoresView(generics.ListAPIView):
    """View for searching stores."""
    serializer_class = StoreListSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Store.objects.filter(name__icontains=query, status='active')
        return Store.objects.none()

class StoreStatsView(APIView):
    """View for store statistics."""
    permission_classes = [IsAuthenticated]

    def get(self, request, store_id):
        try:
            store = Store.objects.get(id=store_id, owner=request.user)
            
            # Get today's date
            today = timezone.now().date()
            
            # Calculate daily sales
            daily_sales = StoreProduct.objects.filter(
                store=store,
                created_at__date=today
            ).count()
            
            # Calculate total revenue
            total_revenue = store.total_sales
            
            # Get product statistics
            total_products = StoreProduct.objects.filter(store=store).count()
            available_products = StoreProduct.objects.filter(
                store=store,
                is_available=True
            ).count()
            
            # Get review statistics
            average_rating = StoreReview.objects.filter(
                store=store
            ).aggregate(Avg('rating'))['rating__avg'] or 0
            
            return Response({
                'daily_sales': daily_sales,
                'total_revenue': total_revenue,
                'total_products': total_products,
                'available_products': available_products,
                'total_reviews': store.total_reviews,
                'average_rating': round(average_rating, 1)
            })
            
        except Store.DoesNotExist:
            return Response(
                {'error': 'Store not found'},
                status=status.HTTP_404_NOT_FOUND
            )
