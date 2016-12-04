import os
from .utils import get_env_variable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY="helloworld"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'hopestarter',
    'hopespace',
    'hopebase',
    'hopepartner',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'hopestarter.urls.main'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hopestarter.context_processors.template_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'hopestarter.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': get_env_variable("PGDATABASE", "hopestarter"),
        'USER': get_env_variable("PGUSER"),
        'PASSWORD': get_env_variable("PGPASS"),
        'HOST': get_env_variable("PGHOST", "localhost"),
        'PORT': get_env_variable("PGPORT", "5432"),
    }
}

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (

)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "site", "static"))
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".." "site", "media"))

NAME_MAX = 100

DEFAULT_PROFILE_IMAGE = 'https://raw.githubusercontent.com/hopestarter/hopestarterapp/master/src/hopestarter/static/img/avatar_b.png'
