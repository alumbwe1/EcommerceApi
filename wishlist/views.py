
from rest_framework import generics, status # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.response  import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.db.models import Count # type: ignore # 
from . import models
from . import serializers
from posts.models import Product
# Create your views here.
class GetLikesCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        likes_count = models.Wishlist.objects.filter(product_id=product_id).count()
        return Response({"likes_count": likes_count})
    
class GetReactsList(generics.ListAPIView):
    serializer_class = serializers.WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Wishlist.objects.filter(user=self.request.user)


class toggleProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        product_id = request.query_params.get('id')

        if not product_id:
            return Response({"message": "Product ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Toggle product reaction
        reaction_item, created = models.Wishlist.objects.get_or_create(
            user=request.user, product=product
        )

        if created:
            return Response({"message": "Product reaction created"}, status=status.HTTP_201_CREATED)
        else:
            reaction_item.delete()
            return Response({"message": "Product reaction removed"}, status=status.HTTP_200_OK)
        
class CheckItemInWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product):
        user = request.user
        in_wishlist = models.Wishlist.objects.filter(user=user, product__id=product).exists()
        return Response({'in_wishlist': in_wishlist}, status=status.HTTP_200_OK)