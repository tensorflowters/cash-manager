
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Manager(BaseUserManager):

		def create_user(self, username, email, password=None):
				if not username:
						raise ValueError('Users must have an username')
				if not email:
						raise ValueError('Users must have an email address')
				if not password:
						raise ValueError('Users must have a password')
				user = self.model(
						username=username,
						email=email,
				)
				user.set_password(password)
				user.save(using=self._db)
				return user

		def create_superuser(self, username, email, password):
				if not username:
						raise ValueError('Users must have an username')
				if not email:
						raise ValueError('Users must have an email address')
				if not password:
						raise ValueError('Users must have a password')
				user = self.create_user(
						username,
						password=password,
						email=email,
				)
				user.is_superuser = True
				user.save(using=self._db)
				return user


class User(AbstractBaseUser):
		username = models.CharField(max_length=255, unique=True, blank=False, null=False)
		email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
		first_name = models.CharField(default='', max_length=255, blank=True, null=False)
		last_name = models.CharField(default='', max_length=255, blank=True, null=False)
		is_staff = models.BooleanField(default=False, blank=False, null=False)
		is_superuser = models.BooleanField(default=False, blank=False, null=False)
		is_active = models.BooleanField(default=True, blank=False, null=False)
		last_login = models.DateTimeField(default=None, null=True, blank=True)

		USERNAME_FIELD = 'username'
		REQUIRED_FIELDS = ['email']

		objects = Manager()

		def __repr__(self):
				return str(self)

		def get_obj(self):
				return {
					"id": self.id,
					"username": self.username,
					"email": self.email,
					"first_name": self.first_name,
					"last_name": self.last_name,
					"is_staff": self.is_staff,
					"is_superuser": self.is_superuser,
					"is_active": self.is_active,
					"last_login": self.last_login
				}

		def get_str(self):
				return (
					f'User(id={self.id}, username={self.username}, email={self.email}, ' \
					f'first_name={self.first_name}, last_name={self.last_name}, is_staff={self.is_staff}, ' \
					f'is_superuser={self.is_superuser}, is_active={self.is_active}, last_login={self.last_login})' \
				)
