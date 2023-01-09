import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from authentication.models import User
from store.models import Cart, Transaction, CartArticle
from store.serializers import CartSerializer, CartArticleSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = "whsec_mBiM0dbNENeGsFxrWmPzuGdLDjCrsigQ"

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
	template_name = 'landing.html'

	@swagger_auto_schema(tags=["Authenticated payments"])
	def get(self, request):
		cart = Cart.objects.all().filter(request.user).first()
		serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)
		return Response({'cart': serialized_cart, 'CHECKOUT_SESSION_URL': settings.CHECKOUT_SESSION_URL },status=status.HTTP_200_OK, template_name='landing.html')


@method_decorator(name="create", decorator=login_required(login_url=f'{settings.API_BASE_URL}/api/login'))
class CheckoutSessionViewset(mixins.CreateModelMixin, GenericViewSet):

	serializer_class = CartSerializer
	queryset = Cart.objects.all()

	# @method_decorator(csrf_exempt)
	# @swagger_auto_schema(tags=["Authenticated payments"])
	# def list(self, request):
	# 	queryset = self.queryset.filter(user=1)

	# 	if queryset.exists():
	# 		cart = queryset.first()
	# 		serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)
	# 		pay_data = []

	# 		for art in serialized_cart["articles"]:
	# 			pay_data.append({
	# 				"price_data": {
	# 					"currency": "usd",
	# 					"product_data": {
	# 						"name": art["article"]["name"],
	# 						"images": [art["article"]["url"]]
	# 					},
	# 					"unit_amount": round(round(float(art["article"]["price"]), 2) * 100) ## In cents,
	# 				},
	# 				"quantity": art["quantity"]
	# 			})

	# 		if len(pay_data) > 0:
	# 			customer = stripe.Customer.create(
	# 				email="superadmin@dev.org",
	# 				metadata={
	# 					"id": 1
	# 				}
	# 			)
	# 			customer_id = customer["id"]
	
	# 			checkout_session = stripe.checkout.Session.create(
	# 				line_items=pay_data,
	# 				mode="payment",
	# 				success_url=f"{settings.API_BASE_URL}/api/authenticated/cart-checkout/success",
	# 				cancel_url=f"{settings.API_BASE_URL}/api/authenticated/cart-checkout/failure",
	# 				customer=customer_id
	# 			)

	# 			return redirect(checkout_session.url, code=303)

	# 		else:
	# 			raise NotFound('No article in cart', code='not_found')
		
	# 	else:
	# 		raise NotFound('No cart found', code='not_found')
	

	@method_decorator(csrf_exempt)
	@swagger_auto_schema(tags=["Authenticated payments"])
	def create(self, request):
		queryset = self.queryset.filter(user=request.user)

		if queryset.exists():
			cart = queryset.first()
			serialized_cart = Cart.get_articles(cart, self.serializer_class, CartArticleSerializer)
			amount = 0

			for art in serialized_cart["articles"]:
				amount = round((amount + float(art["article"]["price"])), 2)

			if amount > 0:
				customer = stripe.Customer.create(
					email="superadmin@dev.org",
					metadata={
						"id": request.user
					}
				)
				customer_id = customer["id"]
	
				try:
					# Create a PaymentIntent with the order amount and currency
					amount = int(round(amount*100, 0))
					paymentIntent = stripe.PaymentIntent.create(
							amount=amount,
							currency='usd',
							automatic_payment_methods={
									'enabled': True,
							},
							customer=customer_id
					)

					ephemeralKey = stripe.EphemeralKey.create(
						customer=customer['id'],
						stripe_version='2022-11-15',
					)
					
					return Response({ 
						"paymentIntent": paymentIntent.client_secret,
						"ephemeralKey": ephemeralKey.secret,
						"customer": customer_id,
						"publishableKey": settings.STRIPE_ACCESS_KEY,
						}, 
						status=status.HTTP_200_OK
					)

				except Exception as e:
						raise ParseError({ 'message': e, 'error': 'Payment creation failed' }, code='validation_error')

			else:
				raise NotFound('No article in cart', code='not_found')
		
		else:
			raise NotFound('No cart found', code='not_found')


class OrderManagerView(APIView):

	def post(self, request):
		payload = request.body
		sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
		event = None

		try:
			event = stripe.Webhook.construct_event(
				payload, sig_header, endpoint_secret
			)

			session = event['data']['object']

			transaction_status = 'AW'
			if session['status'] == 'failed':
				transaction_status = 'FL'
			elif session['status'] == 'succeeded':
				transaction_status = 'SC'
			transaction_amount = round(float(session['amount'])/100, 2)
			transaction_user_email = session['billing_details']['email']

			try:
				new_transaction = create_transaction(transaction_status, transaction_amount, transaction_user_email)

				if session['status'] == 'succeeded':
					user = User.objects.filter(email=transaction_user_email)
					user_id = user.first().id
					user_cart = Cart.objects.filter(user=user_id).first()
					user_cart.total_amount = 0
					user_cart.save()
					user_cart_id = user_cart.id
					articles_to_remove = CartArticle.objects.filter(cart=user_cart_id)
					articles_to_remove.delete()

			except:
				raise ParseError({ "message": "Invalid payload", "error": e }, code='validation_error')
			
			return Response({ "webhook": payload }, status=status.HTTP_200_OK)

		except ValueError as e:
			# Invalid payload
			raise ParseError({ "message": "Invalid payload", "error": e }, code='validation_error')

		except stripe.error.SignatureVerificationError as e:
			# Invalid signature
			raise ParseError({ "message": "Invalid signature", "error": e }, code='validation_error')


def create_transaction(status, amount, user_email):
	transaction = Transaction.objects.create(status=status, amount=amount, payment_user_email=user_email)
	transaction.save()
	return transaction