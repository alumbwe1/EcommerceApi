from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('v1.0/admin/', admin.site.urls),
    path('v1.0/cart/', include('cart.urls')),
    path('v1.0/address/',include('extras.urls')),
    path('v1.0/orders/',include('orders.urls')),
    path('v1.0/wishlist/', include('wishlist.urls')),
    path('v1.0/products/', include('posts.urls')),  
    path('v1.0/auth/', include('djoser.urls')),  
    path('v1.0/auth/', include('djoser.urls.authtoken')), 
]

# This allows serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
