from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from store.views import CategoryViewset
from store.views import ProductViewset
from store.views import ArticleViewset
 
router = routers.SimpleRouter()
router.register('categories', CategoryViewset, basename='categories')
router.register('products', ProductViewset, basename='products')
router.register('articles', ArticleViewset, basename='articles')
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls))
]
