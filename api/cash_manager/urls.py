from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from authentication.views import PublicUserViewset
from authentication.views import AuthenticatedUserViewset
from authentication.views import AdminUserViewset
from store.views import ReadOnlyCategoryViewset
from store.views import ReadOnlyProductViewset
from store.views import ReadOnlyArticleViewset
from store.views import ProductViewset
from store.views import CategoryViewset
from store.views import ArticleViewset
from store.views import StripeView
from store.views import StripeSessionView

router = routers.DefaultRouter(trailing_slash=False)

router.register('api/users', PublicUserViewset, basename='users')

router.register('api/authenticated/users',
                AuthenticatedUserViewset, basename='authenticated-users')

router.register('api/admin/users', AdminUserViewset, basename='admin-users')


router.register('api/categories', ReadOnlyCategoryViewset,
                basename='categories')
router.register('api/products', ReadOnlyProductViewset, basename='products')
router.register('api/articles', ReadOnlyArticleViewset, basename='articles')

router.register('api/admin/categories', CategoryViewset,
                basename='admin-category')
router.register('api/admin/products', ProductViewset,
                basename='admin-products')
router.register('api/admin/articles', ArticleViewset, basename='admin-article')

# router.register('admin/stripe_pk', AdminStripeViewset, basename='admin-stripe')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('stripe-pk/', StripeView.as_view(), name='stripe'),
    path('stripe-session/', StripeSessionView.as_view(), name='stripe-session'),
    path('', include(router.urls))
]
