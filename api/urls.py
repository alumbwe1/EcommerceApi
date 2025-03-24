from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('address/',include('extras.urls')),
    path('orders/',include('orders.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('products/', include('posts.urls')),  
    path('auth/', include('djoser.urls')),  
    path('auth/', include('djoser.urls.authtoken')), 
]

# This allows serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
