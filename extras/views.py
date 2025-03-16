from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from . import models, serializers
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.conf import settings
# Create your views here.


class AddAdress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        user_address = models.Address.objects.create(
            user = request.user,
            lat = data['lat'],
            lng = data['lng'],
            isDefault = data['isDefault'],
            address = data['address'],
            phone = data['phone'],
            addressType = data['addressType']

        )
        if user_address.isDefault == True:
            models.Address.objects.filter(user=request.user).update(isDefault=False)

        user_address.save()

        return Response(status=status.HTTP_201_CREATED)

class GetUserAddres(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = models.Address.objects.filter(user=request.user)
        serializer = serializers.AddressSerializer(addresses, many=True)

        return Response(serializer.data)


class GetDefaultAddress(APIView):
    def get(self, request):
        # Get a QuerySet of addresses instead of a single object
        addresses = models.Address.objects.filter(user=request.user, isDefault=True)

        # Check if any address exists
        if addresses.exists():
            # Retrieve the first item from the QuerySet
            address = addresses.first()
            serializer = serializers.AddressSerializer(address)
            return Response(serializer.data)
        else:
            return Response({'message': 'No default address found'})

        
class DeleteAddress(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        address_id = request.query_params.get('id')

        if not address_id:
            return Response({'message': 'No id provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            address_item = models.Address.objects.get(id=address_id, user=user)
            
            with transaction.atomic():
                # If the address is the default address
                if address_item.isDefault:
                    other_addresses = models.Address.objects.filter(user=user).exclude(id=address_id)
                    
                    if other_addresses.exists():
                        new_default_address = other_addresses.first()
                        new_default_address.isDefault = True
                        new_default_address.save()
                    else:
                        return Response(
                            {'message': 'Cannot delete the default address without any other address'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                # Delete the address
                address_item.delete()
                return Response({'message': 'Address deleted successfully'}, status=status.HTTP_200_OK)

        except models.Address.DoesNotExist:
            return Response({'message': 'Address does not exist'}, status=status.HTTP_404_NOT_FOUND)

class SetDefaultAddress(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        address_id = request.query_params.get('id')

        if not address_id:
            return Response({'message': 'No id provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            address = models.Address.objects.get(id=address_id, user=user)
            models.Address.objects.filter(user=user).update(isDefault=False)
            address.isDefault = True
            address.save()
            return Response({'message': 'Default address updated successfully'}, status=status.HTTP_200_OK)

        except models.Address.DoesNotExist:
            return Response({'message': 'Address does not exist'}, status=status.HTTP_404_NOT_FOUND)
      