from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated, PermissionDenied, NotFound, ParseError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from authentication.models import User
from authentication.permissions import IsAdminAuthenticated, IsStaffAuthenticated, IsUserAuthenticated
from authentication.serializers import UserDetailSerializer, UserSerializer, UserAuthSerializer, UserAuthSerializerPATCH, \
									   RegistrationSerializer, LoginSerializer, RefreshResponseSerializer, PasswordAuthSerializer, \
										 UserDetailSerializerPATCH, UserDetailSerializerPOST
from authentication.utils import get_tokens_for_user
from store.models import Cart

class RegisterViewset(mixins.CreateModelMixin, GenericViewSet):

	serializer_class = RegistrationSerializer
	queryset = User.objects.all()

	@swagger_auto_schema(tags=["Authentication"])
	def create(self, request):
		serializer = RegistrationSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			user_id = user['id']
			cart = Cart.objects.create(user=User.objects.get(pk=user_id))
			cart.save()
			return Response(user, status=status.HTTP_201_CREATED)
		raise ValidationError(serializer.errors, code="validation_error")


class LoginViewset(mixins.CreateModelMixin, GenericViewSet):

	serializer_class = LoginSerializer
	queryset = User.objects.all()

	@swagger_auto_schema(tags=["Authentication"])
	def create(self, request):
		if 'username' not in request.data or 'password' not in request.data:
			raise NotAuthenticated("Authentication credentials were not provided.", code="not_authenticated")
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None and user.is_authenticated:
			login(request, user)
			serialized_user = UserDetailSerializer(user)
			auth_data = get_tokens_for_user(request.user)
			return Response({'user': serialized_user.data, **auth_data}, status=status.HTTP_202_ACCEPTED)
		raise AuthenticationFailed("Incorrect authentication credentials.", code="authentication_failed")


class LogoutViewset(mixins.CreateModelMixin, GenericViewSet):

	serializer_class = LoginSerializer
	queryset = User.objects.all()

	@swagger_auto_schema(tags=["Authentication"])
	def create(self, request):
		logout(request)
		return Response({'message': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class RefreshView(TokenRefreshView):

	@swagger_auto_schema(responses={status.HTTP_200_OK: RefreshResponseSerializer}, tags=["Authentication"])
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


class AuthenticatedUserViewset(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):

	serializer_class = UserAuthSerializer
	permission_classes = [IsUserAuthenticated]

	@method_decorator(csrf_exempt)
	def get_queryset(self):
		authenticated_user = self.request.user
		queryset = User.objects.filter(username=authenticated_user)
		return queryset

	@swagger_auto_schema(tags=["Authenticated users"])
	def retrieve(self, request, pk):
		try:
			user = self.get_queryset().get(pk=pk)
			serializer = UserDetailSerializer(user)
			
			return Response(serializer.data, status=status.HTTP_200_OK)
		
		except ObjectDoesNotExist:
			raise PermissionDenied

	@swagger_auto_schema(tags=["Authenticated users"])
	def update(self, request, pk):
		try:
			user = self.get_queryset().get(pk=pk)
			serializer = UserAuthSerializer(user, data=request.data)

			if serializer.is_valid(raise_exception=True):
				if self.request.data.get("password") != None:
					raise ParseError('password: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("is_superuser") != None:
					raise ParseError('is_superuser: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("is_staff") != None:
					raise ParseError('is_staff: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("is_active") != None:
					raise ParseError('is_active: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("last_login") != None:
					raise ParseError('last_login: This field is read-only and cannot be edited.', code='validation_error')
				else:
					username_exists = serializer.check_username_exists(User.get_obj(user)['username'], request.data['username'])
					email_exists = serializer.check_email_exists(User.get_obj(user)['email'], request.data['email'])
					if username_exists:
						raise ValidationError('Username already exists', code="validation_error")
					elif email_exists:
						raise ValidationError('Email already exists', code="validation_error")
					else:
						serializer.save()
						return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
			else:
				raise ValidationError(serializer.errors, code="validation_error")
		
		except ObjectDoesNotExist:
			raise NotFound

	@swagger_auto_schema(tags=["Authenticated users"])
	def partial_update(self, request, pk):
		try:
			user = self.get_queryset().get(pk=pk)
			serializer = UserAuthSerializerPATCH(user, data=request.data)
			
			if serializer.is_valid(raise_exception=True):
				if self.request.data.get("password") != None:
					raise ParseError('password: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("is_superuser") != None:
					raise ParseError('is_superuser: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("is_staff") != None:
					raise ParseError('is_staff: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("is_active") != None:
					raise ParseError('is_active: This field is read-only and cannot be edited.', code='validation_error')
				elif self.request.data.get("last_login") != None:
					raise ParseError('last_login: This field is read-only and cannot be edited.', code='validation_error')
				else:
					if request.data.get('username') != None:
						username_exists = serializer.check_username_exists(User.get_obj(user)['username'], request.data['username'])
						if username_exists:
							raise ValidationError('Username already exists', code="validation_error")
						else:
							serializer.save()
							return Response(serializer.data, status=status.HTTP_200_OK)
					elif request.data.get('email') != None:
						email_exists = serializer.check_email_exists(User.get_obj(user)['email'], request.data['email'])
						if email_exists:
							raise ValidationError('Email already exists', code="validation_error")
						else:
							serializer.save()
							return Response(serializer.data, status=status.HTTP_200_OK)
					else:
						serializer.save()
						return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				raise ValidationError(serializer.errors, code="validation_error")
		
		except ObjectDoesNotExist:
			raise NotFound


	@swagger_auto_schema(tags=["Authenticated users"])
	@method_decorator(csrf_exempt)
	@action(detail=True, methods=['patch'])
	def set_password(self, request, pk):
		try:
			user = self.get_queryset().get(pk=pk)
			if request.user.is_authenticated:
				serializer = PasswordAuthSerializer(data=request.data)
				if serializer.is_valid():
					user.set_password(request.data.get('password'))
					user.save()
					return Response({ "password": "This field was successfully updated"}, status=status.HTTP_202_ACCEPTED)
				else:
					raise ValidationError(serializer.errors, code="validation_error")
			else:
				raise NotAuthenticated("Authentication credentials were not provided.", code="not_authenticated")
		except ObjectDoesNotExist:
			raise NotFound


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Admin users"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Admin users"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Admin users"]))
class AdminUserViewset(ModelViewSet):

	serializer_class = UserDetailSerializer
	queryset = User.objects.all()
	permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

	@swagger_auto_schema(tags=["Admin users"])
	def create(self, request):
		serializer = UserDetailSerializerPOST(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			user_id = user['id']
			cart = Cart.objects.create(user=User.objects.get(pk=user_id))
			cart.save()
			return Response(user, status=status.HTTP_201_CREATED)
		else:
			raise ValidationError(serializer.errors, code="validation_error")


	@swagger_auto_schema(tags=["Admin users"])
	def update(self, request, pk):
		try:
			user = self.queryset.get(pk=pk)
			serializer = self.serializer_class(user, data=request.data)

			if serializer.is_valid(raise_exception=True):
				if self.request.data.get("password") != None:
					raise ParseError('password: This field is read-only and cannot be edited.', code='validation_error')
				else:
					username_exists = serializer.check_username_exists(User.get_obj(user)['username'], request.data['username'])
					email_exists = serializer.check_email_exists(User.get_obj(user)['email'], request.data['email'])
					if username_exists:
						raise ValidationError('Username already exists', code="validation_error")
					elif email_exists:
						raise ValidationError('Email already exists', code="validation_error")
					else:
						serializer.save()
						return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
			else:
				raise ValidationError(serializer.errors, code="validation_error")
		
		except ObjectDoesNotExist:
			raise NotFound

	@swagger_auto_schema(tags=["Admin users"])
	def partial_update(self, request, pk):
		try:
			user = self.queryset.get(pk=pk)
			serializer = UserDetailSerializerPATCH(user, data=request.data)

			if serializer.is_valid(raise_exception=True):
				if self.request.data.get("password") != None:
					raise ParseError('password: This field is read-only and cannot be edited.', code='validation_error')
				else:
					if request.data.get('username') != None:
						username_exists = serializer.check_username_exists(User.get_obj(user)['username'], request.data['username'])
						if username_exists:
							raise ValidationError('Username already exists', code="validation_error")
						else:
							serializer.save()
							return Response(serializer.data, status=status.HTTP_200_OK)
					elif request.data.get('email') != None:
						email_exists = serializer.check_email_exists(User.get_obj(user)['email'], request.data['email'])
						if email_exists:
							raise ValidationError('Email already exists', code="validation_error")
						else:
							serializer.save()
							return Response(serializer.data, status=status.HTTP_200_OK)
					else:
						serializer.save()
						return Response(serializer.data, status=status.HTTP_200_OK)
			else:
				raise ValidationError(serializer.errors, code="validation_error")
		
		except ObjectDoesNotExist:
			raise NotFound

	@swagger_auto_schema(tags=["Admin users"])
	@method_decorator(csrf_exempt)
	@action(detail=True, methods=['patch'])
	def set_password(self, request, pk):
		try:
			user = self.queryset.get(pk=pk)
			if request.user.is_authenticated:
				serializer = PasswordAuthSerializer(data=request.data)
				if serializer.is_valid():
					user.set_password(request.data.get('password'))
					user.save()
					return Response({ "password": "This field was successfully updated"}, status=status.HTTP_202_ACCEPTED)
				else:
					raise ValidationError(serializer.errors, code="validation_error")
			else:
				raise NotAuthenticated("Authentication credentials were not provided.", code="not_authenticated")
		except ObjectDoesNotExist:
			raise NotFound
