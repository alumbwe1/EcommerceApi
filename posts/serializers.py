from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for retrieving user information."""
    
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for retrieving category information."""
    
    class Meta:
        model = models.Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for retrieving brand information."""
    
    class Meta:
        model = models.Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for retrieving product information."""
    brand = BrandSerializer(read_only=True)  
    
    class Meta:
        model = models.Product
        fields = '__all__'
         

class ProductCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new product."""
    
    class Meta:
        model = models.Product
        fields = '__all__'

    def create(self, validated_data):
        product = models.Product.objects.create(**validated_data)
        return product


class BrandCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new brand."""
    
    class Meta:
        model = models.Brand
        fields = '__all__'
        read_only_fields = ['owner']  


class DeliveryBoySerializer(serializers.ModelSerializer):
    """Serializer for retrieving and creating delivery boy information."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = models.DeliveryBoy
        fields = '__all__'
