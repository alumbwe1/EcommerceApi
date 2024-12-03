from rest_framework import serializers # type: ignore
from . import models

class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for product reactions."""
    
    # Read-only fields to represent the associated product details
    id = serializers.ReadOnlyField(source='product.id')
    title = serializers.ReadOnlyField(source='product.title')
    description = serializers.ReadOnlyField(source='product.description')
    stock = serializers.ReadOnlyField(source='product.stock')
    imageUrls = serializers.ReadOnlyField(source='product.imageUrls')
    category = serializers.ReadOnlyField(source='product.category.id')
    colors = serializers.ReadOnlyField(source='product.colors')
    sizes = serializers.ReadOnlyField(source='product.sizes')
    clothesType = serializers.ReadOnlyField(source='product.clothesType')
    brand = serializers.ReadOnlyField(source='product.brand.id')
    rating = serializers.ReadOnlyField(source='product.rating')
    created_at = serializers.ReadOnlyField(source='product.created_at')
    updated_at = serializers.ReadOnlyField(source='product.updated_at')
    is_featured = serializers.ReadOnlyField(source='product.is_featured')
    price = serializers.ReadOnlyField(source='product.price')


    class Meta:
        model = models.Wishlist
        fields = ['id', 'title', 'description', 'imageUrls', 'rating', 'created_at', 'updated_at', 'stock','category','brand','is_featured','price','colors','sizes','clothesType']