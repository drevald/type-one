from django.utils.translation import gettext_lazy as _
import os
import environ

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2

dot_env = str(BASE_DIR.path(".env"))
if os.path.exists(dot_env):
    env.read_env(dot_env)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'bootstrap4',
    'type_one.core',
    'type_one.records',
    'type_one.ingredients',
    'type_one.api',
    'django_extensions',
    'debug_toolbar',
    'locale',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'pytest_drf'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'type_one.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['type_one/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'type_one.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

DATABASES = {
    "default": env.db()
}

SECRET_KEY = 'segretto'

DEBUG = True

AUTH_USER_MODEL = "core.User"

SESSION_SAVE_EVERY_REQUEST = True

ALLOWED_HOSTS = [
    '192.168.0.191',
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    'type-one.herokuapp.com',
    '192.168.113.101',
    '192.168.0.189',
    '192.168.0.148',
    '192.168.0.198',
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOCALE_PATHS = ( 
    os.path.join(str(BASE_DIR), "type_one", "locale"),
)

USE_I18N = True

LANGUAGES = [
  ('en', _('English')),
  ('ru', _('Russian'))
]

STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')

STATIC_URL = STATIC_HOST + '/static/'

STATIC_ROOT = os.path.join(str(BASE_DIR), 'staticfiles')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=100),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1000),
}

USE_TZ = True