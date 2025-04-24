from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
from extras.models import Address
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from extras import models
import uuid
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated

class TransactionList(APIView):
    """
    List all transactions, or create a new transaction.
    """

    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])

def confirm_payment(request):
    try:
        # Get the user's default address or latest one
        address = models.Address.objects.filter(user=request.user).order_by('-isDefault', '-id').first()

        if address:
            phone = address.phone
            surname = address.surname
        else:
            phone = ''
            surname = ''

        context = {
            'user_email': request.user.email,
            'first_name': request.user.username,
            'last_name': surname,        
            'phone': phone,            
        }

        return render(request, 'payments/confirm_payment.html', context)

    except Exception as e:
        # Optionally log the error or show a fallback message
        return render(request, 'payments/confirm_payment.html', {
            'error': 'Could not load user details.',
        })
        address = Address.objects.filter(user=request.user).order_by('-isDefault', '-id').first()

        if address:
            phone = address.phone
            surname = address.surname
        else:
            phone = ''
            surname = ''

        context = {
            'user_email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': surname,        # Using surname from Address
            'phone': phone,              # Using phone from Address
        }

        return render(request, 'payments/confirm_payment.html', context)

    except Exception as e:
        # Optionally log the error or show a fallback message
        return render(request, 'payments/confirm_payment.html', {
            'error': 'Could not load user details.',
        })



@api_view(['POST'])
def save_transaction(request):
    if request.method == 'POST':
        try:
            # Create's  new transaction
            transaction = Transaction.objects.create(
                id=uuid.uuid4(),
                initiatedAt=timezone.now(),
                amount=request.data.get('amount'),
                fee=request.data.get('fee', 0),
                bearer='customer',
                currency=request.data.get('currency', 'ZMW'),
                reference=request.data.get('reference'),
                lencoReference=request.data.get('lencoReference'),
                type=request.data.get('type', 'payment'),
                status=request.data.get('status', 'pending'),
                source=request.data.get('source', 'web'),
                user=request.user
            )
            
            return Response({
                'status': 'success',
                'message': 'Transaction saved successfully',
                'transaction_id': str(transaction.id)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(APIView):
    """
    Retrieve, update or delete a transaction instance.
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Transaction, pk=pk)

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
