from django.urls import path
from . import views


urlpatterns = [
    path('addressList/', views.GetUserAddres.as_view(), name='user-addresses'),
    path('add/', views.AddAdress.as_view(), name='add-address'),
    path('default/', views.SetDefaultAddress.as_view(), name='default-address'),
    path('delete/', views.DeleteAddress.as_view(), name='delete-address'),
    path('me/', views.GetDefaultAddress.as_view(), name='user-address'),
]