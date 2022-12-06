
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Manager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            username=self.username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            email=email,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
		username = models.CharField(
				max_length=255,
				unique=True,
		)
		first_name = models.CharField(max_length=255, blank=True)
		last_name = models.CharField(max_length=255, blank=True)
		email = models.EmailField(max_length=255, unique=True)
		is_staff = models.BooleanField(default=False)
		is_active = models.BooleanField(default=True)
		last_login = models.DateTimeField(null=True, blank=True)
		is_superuser = models.BooleanField(default=False)

		USERNAME_FIELD = 'username'
		REQUIRED_FIELDS = ['email']

		objects = Manager()

		def __str__(self):
				return self.username

		def has_perm(self, perm, obj=None):
				"Does the user have a specific permission?"
				# Simplest possible answer: Yes, always
				return True

		def has_module_perms(self, app_label):
				"Does the user have permissions to view the app `app_label`?"
				# Simplest possible answer: Yes, always
				return True
