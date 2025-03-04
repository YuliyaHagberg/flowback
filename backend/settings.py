"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import sys

import environ
from pathlib import Path


env = environ.Env(DEBUG=(bool, False),
                  LOGGING=(str, 'NONE'),
                  SECURE_PROXY_SSL_HEADERS=(bool, False),
                  DJANGO_SECRET=str,
                  FLOWBACK_URL=(str, None),
                  INSTANCE_NAME=(str, 'Flowback'),
                  PG_SERVICE=(str, 'flowback'),
                  PG_PASS=(str, '.flowback_pgpass'),
                  REDIS_IP=(str, 'localhost'),
                  REDIS_PORT=(str, '6379'),
                  RABBITMQ_BROKER_URL=(str, 'amqp://flowback:flowback@localhost:5672/flowback'),
                  URL_SUBPATH=(str, ''),
                  AWS_S3_ENDPOINT_URL=(str, None),
                  AWS_S3_ACCESS_KEY_ID=(str, None),
                  AWS_S3_SECRET_ACCESS_KEY=(str, None),
                  AWS_S3_STORAGE_BUCKET_NAME=(str, None),
                  AWS_S3_CUSTOM_URL=(str, None),
                  DISABLE_DEFAULT_USER_REGISTRATION=(bool, False),
                  FLOWBACK_DEFAULT_GROUP_JOIN=(str, None),
                  FLOWBACK_ALLOW_DYNAMIC_POLL=(bool, False),
                  FLOWBACK_ALLOW_GROUP_CREATION=(bool, True),
                  FLOWBACK_GROUP_ADMIN_USER_LIST_ACCESS_ONLY=(bool, False),
                  FLOWBACK_DEFAULT_PERMISSION=(str, 'rest_framework.permissions.IsAuthenticated'),
                  PREDICTION_HISTORY_LIMIT=(int, 100),
                  EMAIL_HOST=(str, None),
                  EMAIL_PORT=(str, None),
                  EMAIL_FROM=(str, None),
                  EMAIL_HOST_USER=(str, None),
                  EMAIL_HOST_PASSWORD=(str, None),
                  EMAIL_USE_TLS=(bool, None),
                  EMAIL_USE_SSL=(bool, None),
                  INTEGRATIONS=(list, []),
                  SCORE_VOTE_CEILING=(int, 100),
                  SCORE_VOTE_FLOOR=(int, 0)
                  )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TESTING = sys.argv[1:2] == ['test'] or "pytest" in sys.modules
env.read_env(os.path.join(BASE_DIR, "../../.env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

FLOWBACK_URL = env('FLOWBACK_URL')
INSTANCE_NAME = env('INSTANCE_NAME')
PG_SERVICE = env('PG_SERVICE')
PG_PASS = env('PG_PASS')

ALLOWED_HOSTS = [FLOWBACK_URL or "*"]

CORS_ALLOW_ALL_ORIGINS = not bool(FLOWBACK_URL)
if not CORS_ALLOW_ALL_ORIGINS:
    if env('SECURE_PROXY_SSL_HEADERS'):
        CORS_ALLOWED_ORIGINS = [f'https://{FLOWBACK_URL}', f'wss://{FLOWBACK_URL}']
    else:
        CORS_ALLOWED_ORIGINS = [f'http://{FLOWBACK_URL}', f'ws://{FLOWBACK_URL}']

if env('SECURE_PROXY_SSL_HEADERS'):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

URL_SUBPATH = env('URL_SUBPATH')
INTEGRATIONS = env('INTEGRATIONS')

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'django_extensions',
    'rest_framework.authtoken',
    'django_celery_beat',
    'pgtrigger',
    'oidc_provider',
    'flowback.user',
    'flowback.group',
    'flowback.poll',
    'flowback.chat',
    'flowback.kanban',
    'flowback.notification',
    'flowback.comment',
    'flowback.schedule',
    'flowback.files',
    'drf_spectacular',
    'phonenumber_field',
    ] + env('INTEGRATIONS')


CELERY_BROKER_URL = env('RABBITMQ_BROKER_URL')

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'flowback.common.documentation.CustomAutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        env('FLOWBACK_DEFAULT_PERMISSION'),
    ),
    'EXCEPTION_HANDLER': 'flowback.common.exception_handlers.drf_default_with_modifications_exception_handler'
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Flowback API',
    'DESCRIPTION': 'Documentation for interfacing with Flowback',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

AUTH_USER_MODEL = 'user.User'
DISABLE_DEFAULT_USER_REGISTRATION = env('DISABLE_DEFAULT_USER_REGISTRATION')

if data := env('FLOWBACK_DEFAULT_GROUP_JOIN'):
    FLOWBACK_DEFAULT_GROUP_JOIN = [int(i) for i in env('FLOWBACK_DEFAULT_GROUP_JOIN').split(',')]

else:
    FLOWBACK_DEFAULT_GROUP_JOIN = []

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

MEDIA_ROOT = str(BASE_DIR) + '/media'
MEDIA_URL = '/media/'
STATIC_ROOT = str(BASE_DIR) + '/static'
STATIC_URL = '/static/'


# Optional AWS Storage Manager

aws_check = [env('AWS_S3_ACCESS_KEY_ID'),
             env('AWS_S3_ENDPOINT_URL'),
             env('AWS_S3_SECRET_ACCESS_KEY'),
             env('AWS_S3_STORAGE_BUCKET_NAME')]

if any(aws_check):
    if not all(aws_check):
        raise Exception("Missing environment variables to connect AWS S3 storage")

    INSTALLED_APPS.append('storages')
    AWS_S3_ENDPOINT_URL = f"https://{env('AWS_S3_ENDPOINT_URL')}"
    AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
    aws_media_url = env('AWS_S3_CUSTOM_URL') or f"{env('AWS_S3_ENDPOINT_URL')}/{env('AWS_S3_STORAGE_BUCKET_NAME')}"
    STATIC_URL = f'https://{env("AWS_S3_CUSTOM_URL")}/static/'

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": env('AWS_S3_STORAGE_BUCKET_NAME'),
                "default_acl": "public-read",
                "location": "media",
                "custom_domain": aws_media_url
            }
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": env('AWS_S3_STORAGE_BUCKET_NAME'),
                "default_acl": "public-read",
                "location": "static",
                "custom_domain": aws_media_url
            }
        }
    }


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

WSGI_APPLICATION = 'backend.wsgi.application'

ASGI_APPLICATION = "backend.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(env('REDIS_IP'), env('REDIS_PORT'))],
        },
    },
}


# OIDC Settings
LOGIN_URL = '/accounts/login/'
OIDC_USERINFO = 'backend.oidc_provider_settings.userinfo'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': PG_SERVICE,
            'passfile': PG_PASS,
        },
    }
}

if TESTING:
    with (open(PG_PASS) as pgpass):
        data = pgpass.readlines()[0].replace('\n', '').split(':')
        DATABASES['default']['NAME'] = data[2]
        DATABASES['default']['USER'] = data[3]
        DATABASES['default']['PASSWORD'] = data[4]


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS') or True
EMAIL_USE_SSL = env('EMAIL_USE_SSL') or False
DEFAULT_FROM_EMAIL = env('EMAIL_FROM', default=env('EMAIL_HOST_USER'))


# Poll related settings
SCORE_VOTE_CEILING = env('SCORE_VOTE_CEILING')
SCORE_VOTE_FLOOR = env('SCORE_VOTE_FLOOR')
FLOWBACK_ALLOW_DYNAMIC_POLL = env('FLOWBACK_ALLOW_DYNAMIC_POLL')


# Logging
if env('LOGGING') in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "file": {
                "level": env('LOGGING'),
                "class": "logging.FileHandler",
                "filename": "general.log",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": env('LOGGING'),
                "propagate": True,
            },
        },
    }

    if DEBUG:
        LOGGING['handlers']['console'] = {'class': 'logging.StreamHandler'}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
