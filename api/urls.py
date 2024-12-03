from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('address/',include('extras.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('products/', include('posts.urls')),  # Handles product-related URLs
    path('auth/', include('djoser.urls')),  # Handles authentication-related URLs (Djoser)
    path('auth/', include('djoser.urls.authtoken')),  # Token-based authentication for API
]

# This allows serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
