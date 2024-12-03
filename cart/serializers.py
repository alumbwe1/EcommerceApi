from rest_framework import serializers  # type: ignore
from . import models
from posts.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Use 'product' instead of 'products'

    class Meta:
        model = models.Cart
        exclude = ['created_at', 'updated_at']  # Exclude fields as needed

    def create(self, validated_data):
        # Here we can add custom logic if needed when creating a Cart instance
        return super().create(validated_data)
