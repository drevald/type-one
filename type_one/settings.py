import environ
import os

env = environ.Env()

BASE_LOC = environ.Path(__file__) - 2
dot_env = str(BASE_LOC.path(".env"))
if os.path.exists(dot_env):
    env.read_env(dot_env)

SECRET_KEY = 'key'

DEBUG = True

SITE_ID = 1

DATABASES = {
    "default": env.db()
    }

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap4',
    'type_one.core'
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [str(BASE_LOC.path("type_one").path("templates"))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    }
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

AUTH_USER_MODEL = "core.User"

ROOT_URLCONF = "type_one.urls"

LOGIN_REDIRECT_URL = "/"

STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')

STATIC_URL = STATIC_HOST + '/static/'

STATIC_ROOT = os.path.join(BASE_LOC, 'staticfiles')

CRISPY_TEMPLATE_PACK = 'uni_form'