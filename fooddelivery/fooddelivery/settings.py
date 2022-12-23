"""
Django settings for fooddelivery project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
#import os
import environ
env = environ.Env()
environ.Env.read_env() 
ALLOWED_HOSTS = ['*']
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5%w+k6uvapby0lzinq7&mr0gq7ilkaw!fukx1uf5wz7sj@-8qd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apps',
    'django_filters',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    
    
]
SITE_ID = 1


#AUTH_USER_MODEL = 'apps.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fooddelivery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'fooddelivery.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':env('DATABASE_NAME'),
        'USER':env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASS'),
        'HOST': 'localhost',
        'PORT': '3306', 
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'


#PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
#STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
#STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
           'rest_framework.authentication.BasicAuthentication',
           'rest_framework.authentication.SessionAuthentication',
       ],
}

STRIPE_PUBLISHABLE_KEY = "pk_test_51M0fgRSAmylrNNcmIK8cNLLRNVuyzTm496tK2sE8t8Yowh7m0jlq0moEM6EGYqeSzPbSgAhFaSZU8nwrtyd2IivN00sgZAy9c7"
STRIPE_SECRET_KEY = "sk_test_51M0fgRSAmylrNNcmjMwqYYffTw41dTm5Q6ZhlcqBNUK45H883dusmuz0cfObwNRoDXzeY2jkFsFKuGVfsq9eEIuy0062PGB84t"

GRAPPELLI_ADMIN_TITLE = "Food Delivery App"


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'APP': {
            'client_id': '1889697541379590',
            'secret': '14e24b8feb64ab39fe5a01c49fed4bd7',
            'key': ''
        }
    }
}

#600253207230-s685jg4mkm13v0mg35av15entm3167q1.apps.googleusercontent.com
#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

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '600253207230-s685jg4mkm13v0mg35av15entm3167q1.apps.googleusercontent.com',
            'secret': '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',
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
    }
}