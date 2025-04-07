

from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config,Csv
import os
from dotenv import load_dotenv

load_dotenv()  # This loads your .env file if it exists.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!



PUBLIC_SCHEMA_NAME = 'public'
PUBLIC_SCHEMA_URLCONF = "eshop.public_urls"
ROOT_URLCONF = "eshop.urls"


# Application definition
SHARED_APPS = (
    'django_tenants',                # Required for multi-tenancy
    'django.contrib.admin',          # Admin interface
    'django.contrib.auth',           # User authentication
    'django.contrib.contenttypes',   # Core app required by Django
    'django.contrib.sessions',       # Handles sessions
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static files management
    'cloudinary_storage',            # Shared third-party app for media storage
    'cloudinary',                    # Shared third-party app for media handling
    'base',                          # Shared app (if it contains shared functionality)
    'allauth',                       # Third-party authentication
    'allauth.account',               # Allauth's account management
    'allauth.socialaccount',         # Allauth social login support
    'allauth.socialaccount.providers.google',  # Google login provider
    'rest_framework',
    
)
TENANT_APPS = (
    'products', 
    'cart',
    'searchprod'  ,                
)
INSTALLED_APPS = SHARED_APPS + TENANT_APPS
SOCIALACCOUNT_ADAPTER = 'base.adapters.TenantSocialAccountAdapter'
# settings.py

TENANT_MODEL = 'base.Client'


TENANT_DOMAIN_MODEL = "base.Domain"
BASE_DOMAIN = "eshop-m942.onrender.com"
from decouple import config

SESSION_COOKIE_DOMAIN = "." + BASE_DOMAIN
CSRF_COOKIE_DOMAIN = "." + BASE_DOMAIN
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

LOGIN_URL = '/accounts/login/'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_tenants.middleware.TenantMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.current_request.ThreadLocalMiddleware',
    # Add the required middleware here
    'allauth.account.middleware.AccountMiddleware',  # Required by django-allauth
]


ROOT_URLCONF = 'eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'eshop.wsgi.application'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Override the engine for django-tenants:
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'

DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']
default_app_config = 'base.apps.BaseConfig'


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#uploading files to cloudinary config
import cloudinary
from decouple import config

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
    secure=True,
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
    'SECURE': True,
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth
]

# Mandatory Allauth settings
SITE_ID = 1
LOGIN_REDIRECT_URL = '/profile_creation/'  # Redirect users after successful login
from django_tenants.utils import get_current_tenant

def is_public_request():
    try:
        from django.core.handlers.wsgi import WSGIRequest
        from threading import local
        _thread_locals = local()
        request = getattr(_thread_locals, 'request', None)
        if request and hasattr(request, 'tenant'):
            return request.tenant.schema_name == 'public'
    except:
        return False
    return False

if is_public_request():
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
