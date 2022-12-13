from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from authentication.views import RegisterViewset
from authentication.views import LoginViewset
from authentication.views import LogoutViewset
from authentication.views import RefreshView
from authentication.views import AuthenticatedUserViewset
from authentication.views import AdminUserViewset
from store.views import ReadOnlyCategoryViewset
from store.views import ReadOnlyProductViewset
from store.views import ReadOnlyArticleViewset
from store.views import ProductViewset
from store.views import CategoryViewset
from store.views import ArticleViewset
from store.views import CartViewset
from store.views import CartArticleViewset
from store.views import StripeView
from store.views import StripeSessionView
from store.views import TestStripeView

schema_view = get_schema_view(
   openapi.Info(
      title="Cash manager API",
      default_version='v0',
      description="Routes to access at the Cash manager ressources application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="arthur.bequie@epitech.eu"),
      license=openapi.License(name="Cash manager License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter(trailing_slash=False)

# Public routes for authentication
router.register('api/register', RegisterViewset, basename='authentication-register')
router.register('api/login', LoginViewset, basename='authentication-login')
router.register('api/logout', LogoutViewset, basename='authentication-logout')

# Athenticated routes for user update actions
router.register('api/authenticated/users',
                AuthenticatedUserViewset, basename='authenticated-users')

# Admin routes for any actions
router.register('api/admin/users', AdminUserViewset, basename='admin-users')

# Public routes for store ressources
router.register('api/categories', ReadOnlyCategoryViewset,
                basename='categories')
router.register('api/products', ReadOnlyProductViewset, basename='products')
router.register('api/articles', ReadOnlyArticleViewset, basename='articles')

# User authenticated routes for store ressources
router.register('api/authenticated/cart', CartViewset, basename='carts')
router.register('api/authenticated/cart-articles', CartArticleViewset, basename='cart-articles')

# Admin routes for any store ressources actions
router.register('api/admin/categories', CategoryViewset,
                basename='admin-category')
router.register('api/admin/products', ProductViewset,
                basename='admin-products')
router.register('api/admin/articles', ArticleViewset, basename='admin-article')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/refresh', RefreshView.as_view(), name='token_refresh'),
    path('stripe-pk/', StripeView.as_view(), name='stripe'),
    path('stripe-session/', StripeSessionView.as_view(), name='stripe-session'),
    path('test-stripe/', TestStripeView.as_view(), name='test-stripe'),
    path('', include(router.urls))
]
