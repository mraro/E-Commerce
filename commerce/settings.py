"""
Django settings for commerce project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.messages import constants

# from utility.env_func import string_to_list, get_env_var
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-vf)%*23pnbb36i82nop$-r%-9%y3_@p_+aawi82@weg2aa1(bg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # particular
    "store",
    "authors",
    "tags",
    # debug:
    "debug_toolbar",
    # especial
    "django_sass_compiler",
    "compressor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # was me that add this
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "commerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "base_templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "commerce.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / 'base_static',
]
# STATIC_ROOT serve pra usar o comando  " python manage.py collectstatic "  QUE CRIA O PACOTE DE STATIC
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder',
                       'compressor.finders.CompressorFinder',
                       )
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

# MEDIA URL E MEDIA ROOT SERVEM PARA DEFINIR ONDE SERA SALVO AO ARQUIVOS QUE OS USUARIOS ADICIONAREM
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MESSAGE_TAGS = {
    constants.WARNING: 'message-warning',
    constants.ERROR: 'message-error',
    constants.SUCCESS: 'message-success',
    constants.INFO: 'message-info',
    constants.DEBUG: 'message-debug',
}

INTERNAL_IPS = [
    "127.0.0.1",
]

SASS_COMPILER_ENABLED = True
SASS_COMPILER_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, 'static/sass'),  # Diretório de origem do seu SCSS
]
SASS_COMPILER_OUTPUT_DIR = 'static/css'  # Diretório de destino para os arquivos CSS compilados
