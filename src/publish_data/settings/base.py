"""
Django settings for publish_data project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yx8#%y$tp^nai8qr0u%z30-roqomsu%*_ida4!mj8guyz5c&q('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

REQUIRED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'papertrail',
    'publish_data',
    'userauth',
    'datasets',
    'tasks',
    'stats',
    'api',
    'runtime_config',
    'oauth2_provider',
]

INSTALLED_APPS = REQUIRED_APPS + PROJECT_APPS

AUTH_USER_MODEL = 'userauth.PublishingUser'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'publish_data.middleware.BasicAuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'publish_data.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'assets/govuk_template/templates/govuk_template')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'datasets.context_processors.govuk_overrides',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'publish_data.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

db_url = os.environ.get('DATABASE_URL')
if db_url:
    print("Warning: DATABASE_URL is already set. Value is %s." % db_url)
    import dj_database_url
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
        }
    }


CORS_ORIGIN_ALLOW_ALL = True

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/accounts/signin'


HOMEPAGE_URL = '/'
LOGO_LINK_TITLE = 'Go to the data.gov.uk homepage'
GLOBAL_HEADER_TEXT = 'data.gov.uk'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "assets/govuk_template/static"),
    os.path.join(PROJECT_DIR, "assets"),
]

ES_HOSTS = os.environ.get('ES_HOSTS')
ES_INDEX = os.environ.get('ES_INDEX')

FIND_URL = os.environ.get('FIND_URL')

try:
    from .local_settings import *
except:
    pass

# Make sure ES settings are available and that the hosts settings is a list
# of strings.
if not (ES_HOSTS and ES_INDEX):
    print("You must export ES_HOSTS and ES_INDEX")
    sys.exit(0)

if isinstance(ES_HOSTS, str):
    ES_HOSTS = [h.strip() for h in ES_HOSTS.split(',')]

if not FIND_URL:
    print("You should set FIND_URL to link your datasets to the find-data app")
