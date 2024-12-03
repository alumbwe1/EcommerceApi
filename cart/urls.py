from django.urls import path # type: ignore
from . import views


urlpatterns = [
    path('me/', views.GetUserCart.as_view(), name='get_user_cart'),
    path('add/', views.AddItemToCart.as_view(), name='add_item_to_cart'),
    path('count/', views.CartCount.as_view(), name='get_cart_count'),
    path('update/', views.UpdateCartItemQuantity.as_view(), name='update_cart_item_quantity'),
    path('delete/', views.DeleteCartItem.as_view(), name='remove_item_from_cart'),
    path('cart/check-item/<int:product>/', views.CheckItemInCart.as_view(), name='check_item_in_cart'),
]