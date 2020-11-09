"""
Django settings for foodgram project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e(3#abay!^k*ga@dn(=-2rpzg$xmx+-^!0i%lg*u^*yio(vtzd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", ]

# необходим для debug_toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'users',
    'recipes',
    'api',
    'multiselectfield',
    'sorl.thumbnail',
    'debug_toolbar',
    'rest_framework',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

]

ROOT_URLCONF = 'foodgram.urls'

# необходимо прописать для обращения к templates из корня проекта
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'recipes.context_processors.number',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.'
                'auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.'
                'auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.'
                'auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib'
                '.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# теперь логотип доступен по адресу sitename.ex**/static/**images/logo.png

# адрес директории, куда командой *collectstatic* будет собрана вся статика
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# путь к дирректории для загрузки изображений
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = 'index'
# LOGOUT_REDIRECT_URL = "index"

if DEBUG is True:
    # подключаем движок для сохранения электронных писем в виде файлов
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    # дирректория, куда будут складываться файлы писем
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

# Идентификатор текущего сайта. Необходим для flatpages
SITE_ID = 1

# Logging
if DEBUG is False:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {'console': {'level': 'DEBUG',
                                 'class': 'logging.StreamHandler'}},
        'loggers': {'django.db.backends': {'handlers': ['console'],
                                           'level': 'DEBUG'}},
    }

# Кеширование
CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
}

# API
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework'
                                    '.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ],
    }
