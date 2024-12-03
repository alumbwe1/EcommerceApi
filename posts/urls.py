from django.urls import path

from rest_framework.routers import DefaultRouter # type: ignore
from posts import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)

urlpatterns = router.urls + [
   
    path('categories/', views.CategoryList.as_view(), name='categories'),
    path('categories/home/', views.HomeCategoryList.as_view(), name='categories'),
    path('<int:product_id>/similar/', views.SimilarProducts.as_view(), name='similar-products'),
    path('search/', views.SearchProduct.as_view(), name='search_product'),
    path('category/<int:category_id>/products/', views.ProductsByCategory.as_view(), name='category-products'),
]