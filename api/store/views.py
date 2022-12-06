from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from django.template.backends.django import TemplateHTMLRenderer
from authentication.permissions import IsAdminAuthenticated, IsStaffAuthenticated, IsUserAuthenticated
from store.models import Category, Product, Article, Cart, CartArticle
from store.serializers import CategoryDetailSerializer, CategoryListSerializer,\
    ProductDetailSerializer, ProductSerializer, ArticleSerializer, ArticleDetailSerializer, CartSerializer, CartArticleSerializer
import os
import stripe
import json 
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

class MultipleSerializerMixin:

    detail_serializer_class = None

    @method_decorator(csrf_exempt)
    def get_serializer_class(self):
        if (self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy') and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ReadOnlyCategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        return Category.objects.filter(active=True)


class CategoryViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()


class ReadOnlyProductViewset(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


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

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        queryset = Product.objects.get(pk=pk)
        products = ProductDetailSerializer(queryset)
        return Response(products.data, status=status.HTTP_202_ACCEPTED)


class ReadOnlyArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Article.objects.all()
        product_id = self.request.query_params.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


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


class CartViewset(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsUserAuthenticated]



class CartArticleViewset(ModelViewSet):
    serializer_class = CartArticleSerializer
    permission_classes = [IsUserAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        # article_id = self.request.data.get('article_id')
        # queryset = CartArticle.objects.filter(article=article_id)
        queryset = CartArticle.objects.all()
        return queryset


class TestStripeView(APIView):
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
    def get(self, request):
        config = {"stripe_pk": os.environ.get('STRIPE_SECRET_KEY')}
        return Response(config)

class StripeSessionView(APIView):
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

# class SuccessView(APIView):
#     renderer_classes = (TemplateHTMLRenderer,)

#     def get(self, request):
#         return Response(template_name='success.html')


# class FailureView(APIView):
#     renderer_classes = (TemplateHTMLRenderer,)

#     def get(self, request):
#         return Response(template_name='failure.html')

# class LandingView(APIView):
#     renderer_classes = [TemplateHTMLRenderer]

#     def get(self, request):
#         article = Article.objects.get(name="Test Product")
#         serializer_class = ArticleSerializer(article)
#         print(serializer_class.data['stripe_price_id'])
#         return Response({'article': article }, template_name='landing.html')

