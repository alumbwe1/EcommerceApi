
from . models import Cart,Product,Addon
from . import serializers
from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from rest_framework import status,generics # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore



class AddItemToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Retrieve the product
        try:
            product = Product.objects.get(id=data['product'])
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve add-ons (list of IDs or names)
        addon_input = data.get('addons', [])  # Can be list of IDs or names

        if addon_input:
            if isinstance(addon_input[0], int):  # If list contains IDs
                addons = Addon.objects.filter(id__in=addon_input)
            else:  # If list contains names
                addons = Addon.objects.filter(name__in=addon_input)
        else:
            addons = []

        # Retrieve quantity
        quantity = data.get('quantity', 1)

        # Check if cart item exists
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}  # Default values if creating new
        )

        if not created:
            # Update quantity if cart item already exists
            cart_item.quantity += quantity

        # Update add-ons
        cart_item.save()  # Save first to ensure it has an ID before setting ManyToMany
        cart_item.addons.set(addons)  # Set ManyToMany relationship

        return Response(
            {'message': 'Product added to cart' if created else 'Cart updated'},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class DeleteCartItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart_item_id = request.query_params.get('id')
        
        # Validate cart_item_id
        if not cart_item_id:
            return Response({'error': 'id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Try's to convert id to an integer if it's expected to be numeric
        try:
            cart_item_id = int(cart_item_id)
        except ValueError:
            return Response({'error': 'id must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve and delete the cart item
        cart_item = get_object_or_404(Cart, id=cart_item_id)
        cart_item.delete()
        return Response({'message': 'Cart item successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class CartCount(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        cart_count = cart_items.count()
        return Response({'cart_count': cart_count}, status=status.HTTP_200_OK)

class CheckItemInCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product):
        user = request.user
        # Correctly use the product parameter from the method argument
        in_cart = Cart.objects.filter(user=user, product__id=product).exists()
        return Response({'in_cart': in_cart}, status=status.HTTP_200_OK)
class UpdateCartItemQuantity(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        # Use query_params to access URL parameters
        cart_item_id = request.query_params.get('id')
        count = request.query_params.get('count')

        # Validate that cart_item_id and count are provided
        if not cart_item_id or not count:
            return Response({'error': 'Both id and count parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            count = int(count)  # Convert count to an integer if it's expected to be a number
        except ValueError:
            return Response({'error': 'Count must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the cart item
        cart_item = get_object_or_404(Cart, id=cart_item_id)
      
        # Update the quantity
        cart_item.quantity = count
        cart_item.save()
        return Response({'message': 'Cart item quantity successfully updated'}, status=status.HTTP_200_OK)


class  GetUserCart(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request):
        user = request.user
        
        cart_items = Cart.objects.filter(user=user).order_by('-created_at')
        serializer = serializers.CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
