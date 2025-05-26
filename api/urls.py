from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),
    path('api/v1.0/admin/', admin.site.urls),
    path('api/v1.0/cart/', include('cart.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/v1.0/address/',include('extras.urls')),
    path('api/v1.0/orders/',include('orders.urls')),
    path('api/v1.0/wishlist/', include('wishlist.urls')),
    path('api/v1.0/products/', include('posts.urls')),  
    path('api/v1.0/auth/', include('djoser.urls')),  
    path('api/v1.0/auth/', include('djoser.urls.authtoken')), 
    path('api/v1.0/payments/', include('payments.urls')),
]

# This allows serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
