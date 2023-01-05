from django.conf import settings
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from authentication.views import RegisterViewset
from authentication.views import LoginViewset
from authentication.views import LogoutViewset
from authentication.views import RefreshView
from authentication.views import AuthenticatedUserViewset
from authentication.views import AdminUserViewset
from bank_server.views import StripeView
from bank_server.views import StripeSessionView
from bank_server.views import TestStripeView
from store.views import ReadOnlyCategoryViewset
from store.views import ReadOnlyProductViewset
from store.views import ReadOnlyArticleViewset
from store.views import ProductViewset
from store.views import CategoryViewset
from store.views import ArticleViewset
from store.views import CartViewset


schema_view = get_schema_view(
   openapi.Info(
      title="Cash manager API",
      default_version='v1',
      description="Routes to access Cash manager application ressources",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="arthur.bequie@epitech.eu"),
      license=openapi.License(name="Cash manager License"),
   ),
   public=True,
   url=settings.API_BASE_URL,
)

router = routers.SimpleRouter(trailing_slash=False)

router.register('api/register', RegisterViewset, basename='register')
router.register('api/login', LoginViewset, basename='login')
router.register('api/logout', LogoutViewset, basename='logout')

router.register('api/categories', ReadOnlyCategoryViewset, basename='categories')
router.register('api/products', ReadOnlyProductViewset, basename='products')
router.register('api/articles', ReadOnlyArticleViewset, basename='articles')

router.register('api/authenticated/cart', CartViewset, basename='authenticated-cart')
router.register('api/authenticated/users', AuthenticatedUserViewset, basename='authenticated-users')

router.register('api/admin/categories', CategoryViewset, basename='admin-categories')
router.register('api/admin/products', ProductViewset, basename='admin-products')
router.register('api/admin/articles', ArticleViewset, basename='admin-articles')
router.register('api/admin/users', AdminUserViewset, basename='admin-users')

urlpatterns = [
   path('', include(router.urls)),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/refresh', RefreshView.as_view(), name='token_refresh'),
   path('stripe-pk/', StripeView.as_view(), name='stripe'),
   path('stripe-session/', StripeSessionView.as_view(), name='stripe-session'),
   path('test-stripe/', TestStripeView.as_view(), name='test-stripe'),
]
