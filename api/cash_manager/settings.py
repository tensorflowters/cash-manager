import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

ADMIN_ENABLED = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
API_BASE_URL=os.getenv("BASE_URL")
AUTH_PROFILE_MODULE = 'authentication.User'
AUTH_USER_MODEL = 'authentication.User'
CHECKOUT_SESSION_URL=os.getenv("CHECKOUT_SESSION_URL")
CORS_ALLOWED_ORIGINS = []
DEBUG = int(os.environ.get("DEBUG", default=0))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
ROOT_URLCONF = 'cash_manager.urls'
SECRET_KEY = os.getenv("SECRET_KEY")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STRIPE_ACCESS_KEY = os.environ.get("STRIPE_ACCESS_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = 'cash_manager.wsgi.application'


if DEBUG == 0:
    from cash_manager.settings_prod import *


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
    }
}
DRF_STANDARDIZED_ERRORS = {
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": False,
    "EXCEPTION_FORMATTER_CLASS": "cash_manager.exception_formatter.CustomExceptionFormatter"
}
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'drf_standardized_errors',
    'drf_yasg',
    'store',
    'rest_framework',
    'rest_framework_simplejwt',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
    'PAGE_SIZE': 15,
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=4),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
SWAGGER_SETTINGS =  {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'TAGS_SORTER': 'alpha',
    'APIS_SORTER': None,
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
TEMPLATE_DIRS = (
  os.path.join(BASE_DIR, "templates"),
)