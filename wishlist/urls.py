from django.urls import path # type: ignore
from . import views


urlpatterns = [
  path('me/', views.GetReactsList.as_view(), name ='me'),
  path('toggle/', views.toggleProduct.as_view(), name='add-remove-wishlist'),
  path('products/<int:product_id>/likes/', views.GetLikesCount.as_view(), name='likes-count'),
  path('check-item/<int:product>/', views.CheckItemInWishlist.as_view(), name='check-item'),
]
