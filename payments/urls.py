from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionList.as_view(), name='transaction-list'),
    path('transactions/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),
    path('transactions/create/', views.TransactionList.as_view(), name='transaction-create'), # POST to /transactions/ will be handled here
    path('transactions/update/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-update'), # PUT to /transactions/<pk>/
    path('transactions/delete/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-delete'), # DELETE to /transactions/<pk>/
    path('payments/', views.TransactionList.as_view(), name='transaction-list'),
    path('payments/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),
    path('payments/confirm/', views.confirm_payment, name='confirm-payment'),
    path('payments/save-transaction/', views.save_transaction, name='save-transaction'),
]
