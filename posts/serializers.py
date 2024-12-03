from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for retrieving category information."""
    
    class Meta:
        model = models.Category
        fields = ['id','title','imageUrl']

class BrandSerializer(serializers.ModelSerializer):
    """Serializer for retrieving brand information."""
    
    class Meta:
        model = models.Brand
        fields = ['id','title','imageUrl']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for retrieving product information."""
    
    class Meta:
        model = models.Product
        fields = '__all__'
         

class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new product."""

  

    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        # Directly create the product with the image
        product = models.Product.objects.create(**validated_data)
        return product

