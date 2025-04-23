from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.TransactionList.as_view(), name='transaction-list'),
    #Just for testing purposes
    path('paymentdemo/', views.demo, name='demo'),
    path('transactions/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-detail'),
    path('transactions/create/', views.TransactionList.as_view(), name='transaction-create'), # POST to /transactions/ will be handled here
    path('transactions/update/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-update'), # PUT to /transactions/<pk>/
    path('transactions/delete/<uuid:pk>/', views.TransactionDetail.as_view(), name='transaction-delete'), # DELETE to /transactions/<pk>/
]
