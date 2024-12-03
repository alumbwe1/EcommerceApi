from rest_framework import viewsets, generics, status # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response  import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.db.models import Count # type: ignore

import random

from . import models, serializers


class CategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    

class HomeCategoryList(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    
    def get_queryset(self):
        queryset = models.Category.objects.all()
        queryset = queryset.annotate(random_order=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]

class BrandList(generics.ListAPIView):
    serializers_class = serializers.BrandSerializer
    queryset = models.Brand.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.ProductCreateSerializer  # Serializer for handling product creation with single image
        return serializers.ProductSerializer  # Serializer for retrieving products

    def perform_create(self, serializer):
        serializer.save() 
 



class ProductList(generics.ListAPIView):
    searializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = models.Product.objects.all()
        queryset = queryset.annotater(random_order=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:20]
    
class PopularProductList(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    
    def get_queryset(self):
        queryset = models.Product.objects.all()
        queryset = queryset.annotater(random_order=Count('id'))
        queryset = list(queryset)
        random.shuffle(queryset)
        return queryset[:5]

class SearchProduct(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query:
            return models.Product.objects.filter(title__icontains=query)  # Fixed from 'title_icontains' to 'title__icontains'
        return models.Product.objects.none()

class ProductsByCategory(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            return models.Product.objects.filter(category_id=category_id)
        return models.Product.objects.none()

class SimilarProducts(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        try:
            product = models.Product.objects.get(id=product_id)
        except models.Product.DoesNotExist:
            return models.Product.objects.none()
        
        # Fetch products from the same category, excluding the current product
        return models.Product.objects.filter(category=product.category).exclude(id=product_id)[:5]
