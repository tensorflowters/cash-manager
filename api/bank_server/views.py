import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from store.models import Cart
from store.serializers import CartSerializer, CartArticleSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(name="get", decorator=login_required(login_url=f'{settings.API_BASE_URL}/api/login'))
class CheckoutSuccessView(APIView):

	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'success.html'

	@swagger_auto_schema(tags=["Authenticated payments"])
	def get(self, request):
		return Response({}, status=status.HTTP_200_OK)


@method_decorator(name="get", decorator=login_required(login_url=f'{settings.API_BASE_URL}/api/login'))
class CheckoutFailureView(APIView):

	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'failure.html'

	@swagger_auto_schema(tags=["Authenticated payments"])
	def get(self, request):
		return Response({"LANDING_URL": f'{settings.API_BASE_URL}/api/authenticated/cart-checkout/landing'}, status=status.HTTP_200_OK)


@method_decorator(name="get", decorator=login_required(login_url=f'{settings.API_BASE_URL}/api/login'))
class CheckoutLandingView(APIView):

	serializer_class = CartSerializer
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'failure.html'

	@swagger_auto_schema(tags=["Authenticated payments"])
	def get(self, request):
		cart = Cart.objects.all().filter(user=request.user).first()
		serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)
		return Response({'cart': serialized_cart, 'CHECKOUT_SESSION_URL': settings.CHECKOUT_SESSION_URL },status=status.HTTP_200_OK, template_name='landing.html')


@method_decorator(name="list", decorator=login_required(login_url=f'{settings.API_BASE_URL}/api/login'))
class CheckoutSessionViewset(mixins.ListModelMixin, GenericViewSet):

	serializer_class = CartSerializer
	queryset = Cart.objects.all()

	@method_decorator(csrf_exempt)
	@swagger_auto_schema(tags=["Authenticated payments"])
	def list(self, request):
		queryset = self.queryset.filter(user=request.user)

		if queryset.exists():
			cart = queryset.first()
			serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)
			pay_data = []

			for art in serialized_cart["articles"]:
				pay_data.append({
					"price_data": {
						"currency": "usd",
						"product_data": {
							"name": art["article"]["name"],
							"images": [art["article"]["url"]]
						},
						"unit_amount": round(round(float(art["article"]["price"]), 2) * 100) ## In cents,
					},
					"quantity": art["quantity"]
				})

			if len(pay_data) > 0:

				checkout_session = stripe.checkout.Session.create(
					line_items=pay_data,
					mode="payment",
					success_url=f"{settings.API_BASE_URL}/api/authenticated/cart-checkout/success",
					cancel_url=f"{settings.API_BASE_URL}/api/authenticated/cart-checkout/failure",
				)

				return redirect(checkout_session.url, code=303)

			else:
				raise NotFound('No article in cart', code='not_found')
		
		else:
			raise NotFound('No cart found', code='not_found')


class OrderManagerView(APIView):

	def get(self, request):

		return Response({"webhook": request.data}, status=status.HTTP_200_OK)