from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
from decouple import config, Csv
import os
from dotenv import load_dotenv

load_dotenv()  # This loads your .env file if it exists.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')

# Multi-tenancy settings
PUBLIC_SCHEMA_NAME = 'public'
PUBLIC_SCHEMA_URLCONF = "eshop.public_urls"
ROOT_URLCONF = "eshop.urls"

# Application definition
SHARED_APPS = (
    'django_tenants',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'base',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
)
TENANT_APPS = (
    'products',
    'cart',
    'searchprod',
)
INSTALLED_APPS = SHARED_APPS + TENANT_APPS
SOCIALACCOUNT_ADAPTER = 'base.adapters.TenantSocialAccountAdapter'

TENANT_MODEL = 'base.Client'
TENANT_DOMAIN_MODEL = "base.Domain"
BASE_DOMAIN = "eshop-m942.onrender.com"

SESSION_COOKIE_DOMAIN = "." + BASE_DOMAIN
CSRF_COOKIE_DOMAIN = "." + BASE_DOMAIN
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

LOGIN_URL = '/accounts/login/'

# Global SSL settings – disable global HTTPS enforcement
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_tenants.middleware.TenantMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware to conditionally redirect public tenant to HTTPS
    'middleware.current_request.ConditionalSSLRedirectMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Allauth middleware
]

ROOT_URLCONF = 'eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}
DATABASES['default']['ENGINE'] = 'django_tenants.postgresql_backend'
DATABASE_ROUTERS = ['django_tenants.routers.TenantSyncRouter']
default_app_config = 'base.apps.BaseConfig'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cloudinary config
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

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
SITE_ID = 1
LOGIN_REDIRECT_URL = '/accounts/profile_creation/'

# Logging configuration
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
