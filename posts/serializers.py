from rest_framework import serializers

from . import models


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
        # Directly create the product with the image
        product = models.Product.objects.create(**validated_data)
        return product
    
class BrandCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new product."""

  

    class Meta:
        model = models.Brand
        fields = '__all__'
        read_only_fields = ['owner']  

   

class DeliveryBoySerializer(serializers.ModelSerializer):
    """Serializer for retrieving and creating delivery boy information."""
    
    class Meta:
        model = models.DeliveryBoy
        fields = '__all__'
        read_only_field = ['user']
        
