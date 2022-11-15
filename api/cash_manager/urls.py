from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from store.views import CategoryViewset
from store.views import ProductViewset
from store.views import ArticleViewset
from store.views import AdminCategoryViewset
from store.views import AdminProductViewset
from store.views import AdminArticleViewset
 
router = routers.SimpleRouter()
router.register('categories', CategoryViewset, basename='categories')
router.register('products', ProductViewset, basename='products')
router.register('articles', ArticleViewset, basename='articles')

router.register('admin/categories', AdminCategoryViewset, basename='admin-category')
router.register('admin/products', AdminProductViewset, basename='admin-category')
router.register('admin/articles', AdminArticleViewset, basename='admin-article')
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
