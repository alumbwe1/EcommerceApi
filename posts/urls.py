from django.urls import path

from rest_framework.routers import DefaultRouter 
from posts import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'deliveryauth', views.DeliveryBoyViewSet)


urlpatterns = router.urls + [
    #Create Product
    path('createproduct/', views.CreateOrUpdateProductView.as_view(), name='create-product'),
    #GoogleAunth
    path('googleauth/', views.google_auth, name='google-auth'),
    #HomeBrands
    path('homebrands/', views.HomeBrandList.as_view(), name='home_brands'),
    path('brand/details/', views.BrandDetails.as_view(), name='brand-details'),
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('brand/', views.BrandList.as_view(), name='Brands'),
    path('categories/home/', views.HomeCategoryList.as_view(), name='categories'),
    path('<int:product_id>/similar/', views.SimilarProducts.as_view(), name='similar-products'),
    path('search/', views.SearchProduct.as_view(), name='search_product'),
    path('search/brand/',views.SearchBrand.as_view(),name='search_brand'),
    path('search/<int:brand_id>/products/',views.SearchProductByBrand.as_view(), name='search_product_by_brand'),
    path('brand/<int:brand_id>/products/', views.ProductsByBrand.as_view(), name='brand-products'),
    path('category/<int:category_id>/products/', views.ProductsByCategory.as_view(), name='category-products'),
    path('brands/<int:brand_id>/categories/', views.CategoriesByBrand.as_view(), name='categories-by-brand'),
    path('categories/<int:category_id>/brands/<int:brand_id>/products/', views.ProductsByCategoryAndBrand.as_view(), name='products-by-category-and-brand'),
    path('categories/<int:category_id>/brands/', views.BrandsByCategory.as_view(), name='brands-by-category'),
    path('dashboard/stats/', views.DashboardStats.as_view(), name='dashboard-stats'),
    
    # Delivery Personel endpoints
    path('delivery/earnings/', views.DeliveryBoyEarnings.as_view(), name='delivery-earnings'),
    path('delivery/orders/', views.DeliveryBoyOrders.as_view(), name='delivery-orders'),
    path('delivery/summary/', views.DeliveryBoyOrderSummary.as_view(), name='delivery-summary'),
]