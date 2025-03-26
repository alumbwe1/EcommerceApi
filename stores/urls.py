from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.StoreCategoryViewSet)
router.register(r'', views.StoreViewSet)

# Create nested router for store products and reviews
store_router = DefaultRouter()
store_router.register(r'products', views.StoreProductViewSet, basename='store-products')
store_router.register(r'reviews', views.StoreReviewViewSet, basename='store-reviews')

urlpatterns = [
    # Store categories and stores
    path('', include(router.urls)),
    
    # Store-specific endpoints
    path('stores/<int:store_id>/', include(store_router.urls)),
    
    # Additional store endpoints
    path('my-stores/', views.MyStoresView.as_view(), name='my-stores'),
    path('featured/', views.FeaturedStoresView.as_view(), name='featured-stores'),
    path('search/', views.SearchStoresView.as_view(), name='search-stores'),
    path('stores/<int:store_id>/stats/', views.StoreStatsView.as_view(), name='store-stats'),
]