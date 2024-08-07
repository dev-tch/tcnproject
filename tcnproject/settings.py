"""
Django settings for tcnproject project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from os import path, getenv
# Load environment variables from .env file
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============== < my custom my config > =============
LOGIN_REDIRECT_URL = "tcn:home" 
LOGOUT_REDIRECT_URL = "tcn:login"
AUTH_USER_MODEL = 'tcn.CustomUser'

#================== config smtp server 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST', '')
EMAIL_PORT = int(getenv('EMAIL_PORT'))
EMAIL_USE_TLS = bool(getenv('EMAIL_USE_TLS'))
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')

# ============== < start my custom my config ASGI  > =============
# Django Channels configuration
ASGI_APPLICATION = 'tcnproject.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.pubsub.RedisPubSubChannelLayer',
        'CONFIG': {
            'hosts': [(getenv('REDIS_HOST'), int(getenv('REDIS_PORT')))],  # Adjust host and port as necessary
        },
    },
}
# rest_framework settings 
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
# post axios 
#CSRF_COOKIE_NAME = "XSRF-TOKEN"

# ============== < end my custom my config ASGI  > =============

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v3s5c82n9@7z0$@y-*7x3dpyf!5)ppsv1k0i+(8s9xyyf52!4t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'test-deploy-3to3.onrender.com'] # config CORS


# Application definition

INSTALLED_APPS = [
    'tcn',  # Your app,
    'channels', 
    'corsheaders', # config CORS
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     'whitenoise.runserver_nostatic',  #for config whitenose 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  #for config whitenose 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # config CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# config CORS 
CSRF_TRUSTED_ORIGINS = ['https://test-deploy-3to3.onrender.com', 'http://localhost:8000'] 
CORS_ALLOWED_ORIGINS = ['https://test-deploy-3to3.onrender.com', 'http://localhost:8000']
from corsheaders.defaults import default_headers, default_methods
CORS_ALLOW_HEADERS = list(default_headers) + ['X-Requested-With', 'X-CSRFToken']
CORS_ALLOW_METHODS = list(default_methods) + ['GET', 'POST', 'DELETE', 'OPTIONS']

ROOT_URLCONF = 'tcnproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path.join(BASE_DIR, 'tcn/templates/tcn')],
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

WSGI_APPLICATION = 'tcnproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'ENGINE': getenv('DB_ENGINE'),
        'NAME': getenv('DB_NAME'),  # Replace with your database name
        'USER': getenv('DB_USER'),  # Replace with your database user
        'PASSWORD': getenv('DB_PASSWORD', ''),  # Replace with your database password
        'HOST':  getenv('DB_HOST'),  # Replace with your database host, e.g., 'localhost' or an IP address
        'PORT': getenv('DB_PORT'),  # Replace with your database port (default is 3306)
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = path.join(BASE_DIR, 'static') # for config whitenose
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" # for config whitenose
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
