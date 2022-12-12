from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from authentication.permissions import IsAdminAuthenticated, IsStaffAuthenticated, IsUserAuthenticated
from store.models import Category, Product, Article, Cart, CartArticle
from store.serializers import CategoryDetailSerializer, CategoryListSerializer,\
    ProductDetailSerializer, ProductSerializer, ArticleSerializer, ArticleDetailSerializer, CartSerializer, CartArticleSerializer
import os
import stripe


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')


class MultipleSerializerMixin:

    detail_serializer_class = None

    @method_decorator(csrf_exempt)
    def get_serializer_class(self):
        if (self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy') and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Public categories"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Public categories"]))
class ReadOnlyCategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        return Category.objects.filter(active=True)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Admin categories"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Admin categories"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["Admin categories"]))
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["Admin categories"]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["Admin categories"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Admin categories"]))
class CategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    @swagger_auto_schema(tags=["Admin categories"])
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Public products"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Public products"]))
class ReadOnlyProductViewset(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Admin products"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Admin products"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["Admin products"]))
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["Admin products"]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["Admin products"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Admin products"]))
class ProductViewset(ModelViewSet):

    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        queryset = Product.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @swagger_auto_schema(tags=["Admin products"])
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        queryset = Product.objects.get(pk=pk)
        products = ProductDetailSerializer(queryset)
        return Response(products.data, status=status.HTTP_202_ACCEPTED)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Public articles"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Public articles"]))
class ReadOnlyArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Article.objects.all()
        product_id = self.request.query_params.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Admin articles"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Admin articles"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["Admin articles"]))
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["Admin articles"]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["Admin articles"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Admin articles"]))
class ArticleViewset(ModelViewSet):

    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Article.objects.all()
        product_id = self.request.query_params.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Authenticated carts"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Authenticated carts"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["Authenticated carts"]))
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["Authenticated carts"]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["Authenticated carts"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Authenticated carts"]))
class CartViewset(ModelViewSet):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsUserAuthenticated]


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Authenticated cart articles"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Authenticated cart articles"]))
@method_decorator(name="create", decorator=swagger_auto_schema(tags=["Authenticated cart articles"]))
@method_decorator(name="update", decorator=swagger_auto_schema(tags=["Authenticated cart articles"]))
@method_decorator(name="partial_update", decorator=swagger_auto_schema(tags=["Authenticated cart articles"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Authenticated cart articles"]))
class CartArticleViewset(ModelViewSet):

    serializer_class = CartArticleSerializer
    permission_classes = [IsUserAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = CartArticle.objects.all()
        return queryset


class TestStripeView(APIView):

    @swagger_auto_schema(tags=["Stripe"])
    def post(self, request):
        try:
            test_payment_intent = stripe.PaymentIntent.create(
                amount=1000, currency='pln', 
                payment_method_types=['card'],
                receipt_email='test@example.com')
            return Response(test_payment_intent)
        except Exception as e:
          return Response({"error": e.user_message})
          pass


class StripeView(APIView):

    @swagger_auto_schema(tags=["Stripe"])
    def get(self, request):
        config = {"stripe_pk": os.environ.get('STRIPE_SECRET_KEY')}
        return Response(config)


class StripeSessionView(APIView):

    @swagger_auto_schema(tags=["Stripe"])
    def post(self, request):
        article = Article.objects.get(name='Test Product')
        serializer_class = ArticleSerializer(article)
        pay_data = {
            "price": serializer_class.data['stripe_price_id'],     
            "quantity": 1,
        }
        checkout_session = stripe.checkout.Session.create(
                success_url="http://0.0.0.0:8000/success",
                cancel_url="http://0.0.0.0:8000/cancel",
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    pay_data,
                ]
        )
        return redirect(checkout_session.url)