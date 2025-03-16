from rest_framework import viewsets, generics, status  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from django.db.models import Count  # type: ignore

import random

from . import models, serializers


class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = list(models.Category.objects.all())
        random.shuffle(queryset)
        return queryset[:5]


class BrandList(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer  # ✅ Fixed typo
    queryset = models.Brand.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return serializers.ProductCreateSerializer  # ✅ Serializer for handling product creation
        return serializers.ProductSerializer  # ✅ Serializer for retrieving products

    def perform_create(self, serializer):
        serializer.save()


class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer  # ✅ Fixed typo

    def get_queryset(self):
        queryset = list(models.Product.objects.all())
        random.shuffle(queryset)
        return queryset[:20]


class PopularProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = list(models.Product.objects.all())
        random.shuffle(queryset)
        return queryset[:5]


class SearchProduct(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get("q", None)
        if query:
            return models.Product.objects.filter(title__icontains=query)  
        return models.Product.objects.none()


class ProductsByCategory(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        if category_id:
            return models.Product.objects.filter(category_id=category_id)
        return models.Product.objects.none()

class SearchProductByBrand(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        brand_id = self.kwargs.get("brand_id")
        search_query = self.request.query_params.get("q", None)
        queryset = models.Product.objects.filter(brand_id=brand_id)

        if search_query:
            queryset = queryset.filter(brand__icontains=search_query)  # Corrected lookup
        return queryset


class ProductsByBrand(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        brand_id = self.kwargs.get("brand_id")
        search_query = self.request.query_params.get("search", None)  # Get the search query from the request

        queryset = models.Product.objects.filter(brand_id=brand_id)  # Filter products by brand

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)  # Filter products by search query in title

        return queryset

class SimilarProducts(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
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
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        brand_id = self.kwargs.get("brand_id")
        if brand_id:
            return models.Category.objects.filter(brands__id=brand_id)  
        return models.Category.objects.none()


class ProductsByCategoryAndBrand(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        brand_id = self.kwargs.get("brand_id")
        if category_id and brand_id:
            return models.Product.objects.filter(category_id=category_id, brand_id=brand_id)
        return models.Product.objects.none()

class BrandsByCategory(generics.ListAPIView):
    serializer_class = serializers.BrandSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        if category_id:
            return models.Brand.objects.filter(categories__id=category_id)  # Assuming a ManyToMany relationship
        return models.Brand.objects.none()
