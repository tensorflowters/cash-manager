import stripe
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from store.models import Article
from store.serializers import ArticleSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY

class TestStripeView(APIView):
    def post(self, request):
        try:
            test_payment_intent = stripe.PaymentIntent.create(
                amount=1000, currency='pln', 
                payment_method_types=['card'],
                receipt_email='test@example.com')
            return Response(test_payment_intent)
        except Exception as e:
          # Invalid parameters were supplied to Stripe's API
          return Response({"error": e.user_message})


class StripeView(APIView):
    def get(self, request):
        config = {"stripe_pk": settings.STRIPE_SECRET_KEY}
        return Response(config)


class StripeSessionView(APIView):
    def post(self, request):
        article = Article.objects.get(pk=1)
        serializer_class = ArticleSerializer(article)
        pay_data = {
            # "price": serializer_class.data['stripe_price_id'],     
            "price": 1000,     
            "quantity": 1,
        }
        checkout_session = stripe.checkout.Session.create(
                success_url=f"{settings.API_BASE_URL}/success",
                cancel_url=f"{settings.API_BASE_URL}/cancel",
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