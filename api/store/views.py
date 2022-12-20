from rest_framework import mixins
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import redirect
from django.db.models.query import EmptyQuerySet
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
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
		serializer = self.detail_serializer_class(self.get_object())
		return Response({ "message": "Category disabled with success", "category": serializer.data }, status=status.HTTP_202_ACCEPTED)


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
@method_decorator(name="disable", decorator=swagger_auto_schema(tags=["Admin products"]))
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
		return Response({ "message": "Product disabled with success", "product": products.data}, status=status.HTTP_202_ACCEPTED)


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


@method_decorator(name="list", decorator=login_required(login_url='/api/login'))
@method_decorator(name="add_article", decorator=login_required(login_url='/api/login'))
@method_decorator(name="remove_article", decorator=login_required(login_url='/api/login'))
@method_decorator(name="set_quantity_article", decorator=login_required(login_url='/api/login'))
class CartViewset(mixins.ListModelMixin, GenericViewSet):

	serializer_class = CartSerializer
	permission_classes = [IsUserAuthenticated]

	@method_decorator(csrf_exempt)
	def get_queryset(self):
			queryset = Cart.objects.filter(user=self.request.user)
			return queryset

	@swagger_auto_schema(tags=["Authenticated carts"])
	def list(self, request):
		queryset = self.get_queryset()

		if isinstance(queryset, EmptyQuerySet):
			raise NotFound('No cart found', code='not_found')

		else:
			cart = queryset.first()
			serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)

			return Response(serialized_cart, status=status.HTTP_200_OK)


	@swagger_auto_schema(tags=["Authenticated carts"])
	@method_decorator(csrf_exempt)
	@action(detail=True, methods=['post'], url_path=r'add/(?P<article_id>[^/.]+)', permission_classes=[IsUserAuthenticated])
	def add_article(self, request, pk, article_id):
		queryset = self.get_queryset()

		if isinstance(queryset, EmptyQuerySet):
			raise NotFound('No cart found', code='not_found')

		else:
			cart_user_id = queryset.get().id

			if cart_user_id == int(pk):
					cart = queryset.first()
					article = Article.objects.filter(pk=article_id)
					cart_articles = CartArticle.objects.filter(cart=cart)

					if isinstance(article, EmptyQuerySet):
						raise NotFound('No article found', code='not_found')

					elif isinstance(cart_articles, EmptyQuerySet):
						CartArticle.objects.create(
							article=article.first(), 
							cart=cart
						)
						serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)

						return Response({ "message": "Article added to cart with success", 'cart': serialized_cart }, status=status.HTTP_201_CREATED)

					else:
						cart_article = cart_articles.filter(article=article.first())

						if cart_article.exists():
							quantity = CartArticleSerializer(cart_article.first()).data.get("quantity")
							newQuantity =  quantity + 1
							cart_article.update(quantity=newQuantity)
							serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)

							return Response({ "message": "Article quantity updated with success", 'cart': serialized_cart }, status=status.HTTP_200_OK)

						else:
							CartArticle.objects.create(
								article=article.first(), 
								cart=cart
							)
							serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)

							return Response({ "message": "Article added to cart with success", 'cart': serialized_cart }, status=status.HTTP_201_CREATED)
								
			else:
				raise PermissionDenied

	@swagger_auto_schema(tags=["Authenticated carts"])
	@method_decorator(csrf_exempt)
	@action(detail=True, methods=['delete'], url_path=r'remove/(?P<article_id>[^/.]+)', permission_classes=[IsUserAuthenticated])
	def remove_article(self, request, pk, article_id):
		try:
			cart = Cart.objects.get(pk=pk)
			article = Article.objects.get(pk=article_id)
			card_article = CartArticle.objects.filter(article=article, cart=cart)
			if card_article.exists():
				newQuantity = CartArticleSerializer(
					card_article.first()).data.get("quantity") - 1
				if newQuantity <= 0:
					card_article.delete()
					return Response({"message": "Article removed from cart"}, status=status.HTTP_200_OK)
				else:
					card_article.update(quantity=newQuantity)
					return Response({"message": "Quantity updated", 'card_article': CartArticleSerializer(card_article.get()).data}, status=status.HTTP_200_OK)
			else:
				raise NotFound('No article found in cart', code='not_found')
		
		except ObjectDoesNotExist:
			raise NotFound('No cart or article found', code='not_found')

	@swagger_auto_schema(tags=["Authenticated carts"])
	@method_decorator(csrf_exempt)
	@action(detail=True, methods=['put'], url_path=r'set_quantity/(?P<article_id>[^/.]+)', permission_classes=[IsUserAuthenticated])
	def set_quantity_article(self, request, pk, article_id):
		try:
			cart = Cart.objects.get(pk=pk)
			article = Article.objects.get(pk=article_id)
			card_article = CartArticle.objects.filter(article=article, cart=cart)
			newQuantity = request.data.get("quantity")

			if card_article.exists():
				if newQuantity is not None:
					if isinstance(newQuantity, int) and newQuantity >= 0:
						if newQuantity == 0:
							card_article.delete()
							return Response({"message": "Article removed from cart"}, status=status.HTTP_204_NO_CONTENT)
						else:
							card_article.update(quantity=newQuantity)
							return Response({"message": "Quantity updated", 'card_article': CartArticleSerializer(card_article.first()).data}, status=status.HTTP_200_OK)
					else:
						raise ParseError('Quantity need to be a positive or equal to zero integer', code='parse_error')
				else:
					raise ParseError('Quantity cannot be blank', code='parse_error')
			else:
				if newQuantity is not None:
					if isinstance(newQuantity, int) and newQuantity >= 0:
						if newQuantity != 0:
							new_card_article = CartArticle.objects.create(
								article=article, cart=cart)
							new_card_article = CartArticle.objects.filter(
								article=article, cart=cart)
							new_card_article.update(quantity=newQuantity)
							return Response({"message": "Articled added to cart", 'card_article': CartArticleSerializer(new_card_article.first()).data}, status=status.HTTP_201_CREATED)
						else:
							raise ParseError('Quantity cannot be null', code='parse_error')
					else:
						raise ParseError('Quantity need to be a positive or equal to zero integer', code='parse_error')
				else:
					raise ParseError('Quantity cannot be blank', code='parse_error')
		
		except ObjectDoesNotExist:
			raise

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
