"""
Django settings for pureBeurre project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
import sentry_sdk

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("base", BASE_DIR)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#y-ca+0y#ewq-i=1y*5_fnad8@&r$t%7g@u#$lmg@2k_tu8cms'

ALLOWED_HOSTS = ["127.0.0.1","35.180.64.180"]

LOGIN_URL = 'user/login/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig', 
    'research.apps.ResearchConfig', 
    'skeleton.apps.SkeletonConfig', 
    'products.apps.ProductsConfig', 
    # "django_nose"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'config.urls'

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
                'skeleton.context_processors.get_search_form'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # on utilise l'adaptateur postgresql
        'NAME': 'purebeurre', # le nom de notre base de donnees creee precedemment
        'USER': 'blingstand', # attention : remplacez par votre nom d'utilisateur
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
}}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
#for django-nose
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = [
#     '--with-coverage',
#     '--cover-tests',
#     '--cover-package=user, products, research',
#     '--cover-html'
# ]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'

# Static files settings
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
TATIC_URL = '/static/'

# Static files settings
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
print("settings : ", PROJECT_ROOT)
print("staticfiles", STATIC_ROOT)
# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
#     )
