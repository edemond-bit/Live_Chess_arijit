"""
Django settings for hrsuit project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import sys

import django_heroku
import os

# from .email_info import *
# # Email Settings
# EMAIL_HOST = EMAIL_HOST
# EMAIL_HOST_USER = EMAIL_HOST_USER
# EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
# EMAIL_PORT = EMAIL_PORT
# EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nautiyalakshat7@gmail.com'  # test
EMAIL_HOST_PASSWORD = 'akshatn1111'  # test
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@jdf01zf3u9vyqv62^kjf=f2%^#sh2taf0x=6%#o0-_xa=1gb*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['chess-live-final.herokuapp.com']
ALLOWED_HOSTS = ['*']

# Email Settings
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'edward.mike.anaryo@gmail.com' #test
# EMAIL_HOST_PASSWORD = 'yencommerce'#test
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# FGN FTP Settings
FTP_URL = 'tde-projects.com'
FTP_USER = 'tdeprojects'
FTP_PASSWORD = 'TProDigiRA0434@020892#'

# Payment Gateway Settings
#if (len(sys.argv) >= 2 and sys.argv[1] == 'runserver'):
#    BRAINTREE_PRODUCTION = False
#else:
#    BRAINTREE_PRODUCTION = True
BRAINTREE_PRODUCTION = False
BRAINTREE_MERCHANT_ID = '9h4qs28js633zrwp'
BRAINTREE_PUBLIC_KEY = '48ttbj6m9dyjwwtn'
BRAINTREE_PRIVATE_KEY = 'e994bd2f977a256528937fe146ba46b4'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # INSTALLED APPS
    'crispy_forms',
    'phonenumber_field',
    'widget_tweaks',

    # PROJECT APPS
    'dashboard',
    'accounts',
    'users',
    'tournment',
    'timezone_field',
    'gateway',
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

ROOT_URLCONF = 'hrsuit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'hrsuit.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# STATIC FILES WILL BE SERVED FROM STATIC_CDN WHEN WE ARE LIVE - OUT SIDE OF PROJECT
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn', 'static_root')

# THIS KEEPS THE PROJECT FILES - CSS/JS/IMAGES/FONTS
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_in_proj', 'our_static'),
]

# MEDIA - UPLOADED FILES/IMAGES
MEDIA_URL = '/media/'

# MEDIA FILES WILL BE SERVED FROM STATIC_CDN WHEN WE ARE LIVE
MEDIA_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'media_root')

django_heroku.settings(locals())