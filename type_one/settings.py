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
    'django_extensions',
    'debug_toolbar',
    'locale',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'rest_framework'
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
    'type-one.herokuapp.com'
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
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


