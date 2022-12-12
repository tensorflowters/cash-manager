from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from drf_yasg.utils import swagger_auto_schema
from authentication.utils import get_tokens_for_user
from authentication.models import User
from authentication.permissions import IsAdminAuthenticated, IsStaffAuthenticated, IsUserAuthenticated
from authentication.serializers import UserDetailSerializer, UserDetailSerializerPATCH, UserSerializer, UserAuthSerializer, UserAuthSerializerPATCH, RegistrationSerializer, LoginSerializer, RefreshResponseSerializer, UserLoginResponseSerializer


class RegisterViewset(mixins.CreateModelMixin, GenericViewSet):

    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=["Authentication"])
    def create(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=request.data.get('email')).exists():
                return Response({'email': 'Account with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewset(mixins.CreateModelMixin, GenericViewSet):

    serializer_class = LoginSerializer
    queryset = User.objects.all()

    @swagger_auto_schema(tags=["Authentication"])
    def create(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'message': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        serialized_user = UserLoginResponseSerializer(user)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'message': 'Login Success', 'user': serialized_user.data, **auth_data}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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


class AuthenticatedUserViewset(mixins.UpdateModelMixin, GenericViewSet):

    serializer_class = UserAuthSerializer
    permission_classes = [IsUserAuthenticated]

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        authenticated_id = self.request.user
        queryset = User.objects.filter(username=authenticated_id)
        return queryset

    @swagger_auto_schema(tags=["Authenticated users"])
    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserAuthSerializer(user, data=request.data)

        if serializer.is_valid():
            if self.request.data.get("password") == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'password': "You should use the appropriate url to edit user's password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Authenticated users"])
    def partial_update(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserAuthSerializerPATCH(user, data=request.data)

        if serializer.is_valid():
            if self.request.data.get("password") == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'password': "You should use the appropriate url to edit user's password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Authenticated users"])
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['patch'])
    def set_password(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'password': "Password successfully updated"}, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response('User does not exists', status=status.HTTP_400_BAD_REQUEST)


@method_decorator(name="list", decorator=swagger_auto_schema(tags=["Admin users"]))
@method_decorator(name="retrieve", decorator=swagger_auto_schema(tags=["Admin users"]))
@method_decorator(name="destroy", decorator=swagger_auto_schema(tags=["Admin users"]))
class AdminUserViewset(ModelViewSet):

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

    @swagger_auto_schema(tags=["Admin users"])
    def create(self, request):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email=request.data.get('email')).exists():
                return Response({'email': ['Account with this email already exists']}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(serializer.data.get(
                'username'), serializer.data.get('email'), serializer.data.get('password'))
            user.first_name = serializer.data.get('first_name')
            user.last_name = serializer.data.get('last_name')
            user.save()
            new_user = UserSerializer(user)
            return Response(new_user.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Admin users"])
    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserDetailSerializer(user, data=request.data)

        if serializer.is_valid():
            if self.request.data.get("password") == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'password': ["You should use the appropriate url to edit user's password"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Admin users"])
    def partial_update(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserDetailSerializerPATCH(user, data=request.data)

        if serializer.is_valid():
            if self.request.data.get("password") == None:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'password': ["You should use the appropriate url to edit user's password"]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=["Admin users"])
    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['patch'])
    def set_password(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            new_password = request.data.get('password')
            if new_password is not None and new_password != "":
                user.set_password(new_password)
                user.save()
                return Response({'password': ["Password successfully updated"]}, status=status.HTTP_202_ACCEPTED)
            return Response({'password': ['Please provide a no empty password']}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response('User does not exists', status=status.HTTP_400_BAD_REQUEST)
    