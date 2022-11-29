from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from authentication.permissions import IsAdminAuthenticated, IsStaffAuthenticated
from store.models import Category, Product, Article
from store.serializers import CategoryDetailSerializer, CategoryListSerializer,\
    ProductDetailSerializer, ProductSerializer, ArticleSerializer
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


class ReadOnlyCategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        return Category.objects.filter(active=True)


class ReadOnlyProductViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    detail_serializer_class = ProductDetailSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        queryset = Product.objects.get(pk=pk)
        return Response(queryset)


class ReadOnlyArticleViewset(ReadOnlyModelViewSet):

    serializer_class = ArticleSerializer

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset


class ArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]


class StripeView(APIView):
    def get(self, request, format=None):
        config = {"stripe_pk": os.environ.get('STRIPE_SECRET_KEY')}
        return Response(config)


class StripeSessionView(APIView):
    def get(self, request, format=None):
        body = JSONParser().parse(request)
        return Response(body)
        # pay_data = {
        # "price_data": {
        # "currency": "usd",
        # "unit_amount": body['product_price'],
        #  "product_data": {
        #     "name": body['product_name'],
        #    "images": body['product_image'],
        #  }
        # },
        #  "quantity": 1,
    # }

        # checkout_session = stripe.checkout.Session.create(
        # success_url="",
        # cancel_url="",
        # payment_method_types=['card'],
        # mode='payment',
        # line_items=[
        #    pay_data,
        # ]
       #  )
        # return Response({'sessionId': checkout_session['id']})
