from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from authentication.permissions import IsAdminAuthenticated, IsStaffAuthenticated, IsUserAuthenticated
from authentication.serializers import UserDetailSerializer, UserDetailSerializerPATCH, UserSerializer, UserAuthSerializer, UserAuthSerializerPATCH


class PublicUserViewset(mixins.CreateModelMixin,
                        GenericViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
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
        serializer = UserAuthSerializerPATCH(user, data=request.data)

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


class AdminUserViewset(ModelViewSet):

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminAuthenticated, IsStaffAuthenticated]

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
