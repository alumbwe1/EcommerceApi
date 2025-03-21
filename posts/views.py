from rest_framework import viewsets, generics, status  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated  
from django.db.models import Count  

import random

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
    
    

