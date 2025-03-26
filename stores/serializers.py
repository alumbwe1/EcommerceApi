from rest_framework import serializers
from .models import StoreCategory, Store, StoreProduct, StoreReview
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class StoreCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreCategory
        fields = ['id', 'name', 'description', 'image', 'created_at', 'is_active']

class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = [
            'id', 'store', 'name', 'description', 'price', 'sale_price',
            'stock', 'image', 'category', 'is_available', 'created_at'
        ]

class StoreReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StoreReview
        fields = ['id', 'store', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = StoreCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=StoreCategory.objects.all(),
        write_only=True,
        source='category'
    )
    products = StoreProductSerializer(many=True, read_only=True)
    reviews = StoreReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Store
        fields = [
            'id', 'owner', 'name', 'category', 'category_id', 'description',
            'logo', 'banner', 'address', 'phone', 'email', 'website',
            'opening_time', 'closing_time', 'business_days',
            'rating', 'total_reviews', 'total_sales',
            'status', 'is_featured', 'created_at', 'updated_at',
            'products', 'reviews', 'average_rating'
        ]
        read_only_fields = ['owner', 'rating', 'total_reviews', 'total_sales', 'status']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class StoreListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing stores."""
    category = StoreCategorySerializer(read_only=True)

    class Meta:
        model = Store
        fields = [
            'id', 'name', 'category', 'logo', 'rating',
            'total_reviews', 'is_featured', 'status'
        ]