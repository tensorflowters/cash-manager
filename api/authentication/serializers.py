from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from authentication.models import User


class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(min_length=8, max_length=255, allow_blank=False)

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'first_name', 'last_name']

	def save(self):
		user = User(username=self.validated_data['username'], email=self.validated_data['email'])
		password = self.validated_data['password']
		user.set_password(password)
		user.first_name = self.validated_data.get('first_name', '')
		user.last_name = self.validated_data.get('last_name', '')
		user.save()
		return User.get_obj(user)


class LoginSerializer(serializers.ModelSerializer):
	password = serializers.CharField(min_length=8, max_length=255, allow_blank=False)

	class Meta:
		model = User
		fields = ['username', 'password']


class RefreshResponseSerializer(serializers.Serializer):
	access = serializers.CharField()

	def create(self, validated_data):
		raise NotImplementedError()

	def update(self, instance, validated_data):
		raise NotImplementedError()


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name',
				  'email']


class UserAuthSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'first_name', 'last_name']
		read_only_fields = ['is_staff', 'is_active', 'last_login', 'is_superuser']

	def check_username_exists(self, username, new_username):
		if User.objects.exclude(username=username).filter(username=new_username).exists():
			return True
		else:
			return False

	def check_email_exists(self, email, new_email):
		if User.objects.exclude(email=email).filter(email=new_email).exists():
			return True
		else:
			return False


class UserAuthSerializerPATCH(serializers.ModelSerializer):
	username = serializers.CharField(required=False)
	first_name = serializers.CharField(required=False)
	last_name = serializers.CharField(required=False)
	email = serializers.CharField(required=False)

	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name',
				  'email']


class UserDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name',
				  'email', 'is_staff', 'is_active', 'last_login', 'is_superuser']


class UserDetailSerializerPATCH(serializers.ModelSerializer):

	username = serializers.CharField(required=False)
	first_name = serializers.CharField(required=False)
	last_name = serializers.CharField(required=False)
	email = serializers.CharField(required=False)
	is_staff = serializers.CharField(required=False)
	is_active = serializers.CharField(required=False)
	last_login = serializers.CharField(required=False)
	is_superuser = serializers.CharField(required=False)

	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name',
				  'email', 'is_staff', 'is_active', 'last_login', 'is_superuser']
