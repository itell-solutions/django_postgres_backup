"""
Django settings for example_project project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

_ENVVAR_DPB_SECRET_KEY = "DPB_SECRET_KEY"
_ENVVAR_DPB_ENVIRONMENT = "DPB_ENVIRONMENT"
_ENVVAR_DPB_DEV_DEMO_PASSWORD = "DPB_DEV_DEMO_PASSWORD"
_ENVVAR_DPB_POSTGRES_DATABASE = "DPB_POSTGRES_DATABASE"
_ENVVAR_DPB_POSTGRES_HOST = "DPB_POSTGRES_HOST"
_ENVVAR_DPB_POSTGRES_PASSWORD = "DPB_POSTGRES_PASSWORD"
_ENVVAR_DPB_POSTGRES_PORT = "DPB_POSTGRES_PORT"
_ENVVAR_DPB_POSTGRES_USERNAME = "DPB_POSTGRES_USERNAME"


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-not-a-secret"

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
    "django.contrib.postgres",
    "django_extensions",
    "example_app",
    "django_postgres_backup",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "example_project.wsgi.application"

_DEFAULT_DEMO_PASSWORD = "not-secret"
DEMO_PASSWORD = os.environ.get(_ENVVAR_DPB_DEV_DEMO_PASSWORD, _DEFAULT_DEMO_PASSWORD)

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
_DEFAULT_POSTGRES_DATABASE = "dpb"
_DEFAULT_POSTGRES_HOST = "localhost"
_DEFAULT_POSTGRES_PASSWORD = DEMO_PASSWORD
_DEFAULT_POSTGRES_PORT = "5444"
_DEFAULT_POSTGRES_USERNAME = "postgres"
_POSTGRES_DATABASE = os.environ.get(_ENVVAR_DPB_POSTGRES_DATABASE, _DEFAULT_POSTGRES_DATABASE)
_POSTGRES_HOST = os.environ.get(_ENVVAR_DPB_POSTGRES_HOST, _DEFAULT_POSTGRES_HOST)
_POSTGRES_PASSWORD = os.environ.get(_ENVVAR_DPB_POSTGRES_PASSWORD, _DEFAULT_POSTGRES_PASSWORD)

if _POSTGRES_PASSWORD is None:
    raise ValueError(f"environment variable {_ENVVAR_DPB_POSTGRES_PASSWORD} must be set")
_POSTGRES_PORT = int(os.environ.get(_ENVVAR_DPB_POSTGRES_PORT, _DEFAULT_POSTGRES_PORT))
_POSTGRES_USERNAME = os.environ.get(_ENVVAR_DPB_POSTGRES_USERNAME, _DEFAULT_POSTGRES_USERNAME)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _POSTGRES_DATABASE,
        "USER": _POSTGRES_USERNAME,
        "PASSWORD": _POSTGRES_PASSWORD,
        "HOST": _POSTGRES_HOST,
        "PORT": _POSTGRES_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

POSTGRES_BACKUP_GENERATIONS = 3
