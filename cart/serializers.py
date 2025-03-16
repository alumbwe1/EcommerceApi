from rest_framework import serializers  # type: ignore
from . import models
from posts.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  

    class Meta:
        model = models.Cart
        #No need for these bullshit
        exclude = ['created_at', 'updated_at']  

    def create(self, validated_data):
        # Some other logic if needed
        return super().create(validated_data)
