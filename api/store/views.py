from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import mixins
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from store.permissions import IsAdminAuthenticated, IsStaffAuthenticated, IsUserAuthenticated
from django.contrib.auth.models import User
from store.models import Category, Product, Article
from store.serializers import CategoryDetailSerializer, CategoryListSerializer,\
    ProductDetailSerializer, ProductSerializer, ArticleSerializer, UserSerializer, UserDetailSerializer, UserAuthSerializer
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


class UserViewset(ModelViewSet):

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]


class PublicUserViewset(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(serializer.data.get(
                'username'), serializer.data.get('email'), serializer.data.get('password'))
            user.first_name = serializer.data.get('first_name')
            user.last_name = serializer.data.get('last_name')
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticatedUserViewset(mixins.UpdateModelMixin, GenericViewSet):

    serializer_class = UserAuthSerializer
    permission_classes = [IsUserAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        authenticated_id = self.request.user
        queryset = User.objects.filter(username=authenticated_id)
        return queryset

    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserAuthSerializer(user, data=request.data)

        if serializer.is_valid():
            if self.request.data.get("password") == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'password': ["You should use the appropriate url to edit user's password"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserAuthSerializer(user, data=request.data)

        if serializer.is_valid():
            if self.request.data.get("password") == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'password': ["You should use the appropriate url to edit user's password"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['patch'])
    def set_password(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'password': ["Password successfully updated"]}, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response('User does not exists', status=status.HTTP_400_BAD_REQUEST)


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

class SuccessView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name='success.html')


class FailureView(APIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name='failure.html')

class LandingView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        article = Article.objects.get(name="Test Product")
        serializer_class = ArticleSerializer(article)
        print(serializer_class.data['stripe_price_id'])
        return Response({'article': article }, template_name='landing.html')

