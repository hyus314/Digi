"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jg(ht&70ap2!f(&5s-d28hh$uz2m09p)ytwjk*-p$v6x(a4puf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '127.0.0.2', '127.0.0.3']


import os
from cryptography.fernet import Fernet

# Retrieve the Fernet key from an environment variable or generate a new one
FERNET_KEY = os.environ.get('FERNET_KEY', Fernet.generate_key().decode())

# Ensure the key is byte-encoded for use in Fernet
cipher_suite = Fernet(FERNET_KEY.encode())

# Application definition

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'chat.apps.ChatConfig',
    'accounts.apps.AccountsConfig',
    'tokens.apps.TokensConfig',
    'connections.apps.ConnectionsConfig',
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "Digi",
        "HOST": "DESKTOP-85Q0589\\SQLEXPRESS",
        "TRUSTED_CONNECTION": "yes",
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server", 
        },
    },
    #  'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'Digi', 
    #     'USER': 'user', 
    #     'PASSWORD': 'DigiPassword12',  
    #     'HOST': '127.0.0.1',  
    #     'PORT': '3306',  
    # }
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

CELERY_BROKER_URL = 'amqp://guest:guest@localhost'
CELERY_RESULT_BACKEND = 'django-db'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ASGI_APPLICATION = 'main.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  
        },
    },
}