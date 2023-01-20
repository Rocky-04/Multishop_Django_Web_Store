import os.path
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from config import DATABASE_PASSWORD, DATABASE_NAME, DATABASE_HOST, DATABASE_PORT
from config import EMAIL_HOST_PASSWORD
from config import EMAIL_HOST_USER
from config import SECRET_KEY
from config import SERVER_EMAIL

BASE_DIR = Path(__file__).resolve().parent.parent

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECRET_KEY = SECRET_KEY

DEBUG = True

ALLOWED_HOSTS = ['multishop.pp.ua', 'www.multishop.pp.ua', '127.0.0.1', 'testserver', 'rocky.pp.ua']

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'debug_toolbar',
    'cachalot',
    'ckeditor',
    'mptt',
    'nested_admin',
    'captcha',

    'shop.apps.ShopConfig',
    'favorite',
    'basket',
    'users',
    'orders',
    'news',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'online_store.middleware.SessionAuthenticationMiddleware',
    'online_store.middleware.ExceptionLoggingMiddleware'
]

ROOT_URLCONF = 'online_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'basket.context_processors.basket_products_context',
                'favorite.context_processors.favorite_products_context',
                'users.context_processors.get_newsletter_subscription_form_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'online_store.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_NAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
        'ATOMIC_REQUEST': False,
    },
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_data',
        'ATOMIC_REQUESTS': False,
    }

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

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukraine')),
)

TIME_ZONE = 'EET'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
if DEBUG:
    STATIC_ROOT = ''
    STATICFILES_DIRS = (os.path.join('static'),)
else:
    # STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_ROOT = '/var/www/static'

MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = '/var/www/media'

EMPTY_IMAGE = '/media/images/empty/empty.png'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ['127.0.0.1']

CKEDITOR_UPLOAD_PATH = "uploads/"

LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.ukr.net'
EMAIL_PORT = 465
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
SERVER_EMAIL = SERVER_EMAIL
ADMINS = [
    ('Rocky', 'rocky01396@gmail.com'),
    ('Frank', "rocky113@ukr.net"),
]

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

CAPTCHA_FONT_SIZE = 40
CAPTCHA_IMAGE_SIZE = (120, 50)
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

LOG_ROOT = os.path.join(BASE_DIR, 'logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_ROOT + '/logs.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'root': {
            'handlers': ['mail_admins', 'console', 'file'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

CELERY_BROKER_URL = 'redis://redis:6379/0'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379',
        'OPTIONS': {
            'db': '1',
        }
    }
}
