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

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }    

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.sessions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'type_one.core'
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
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
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

AUTH_USER_MODEL = "core.User"

ROOT_URLCONF = "type_one.urls"

LOGIN_REDIRECT_URL = "/"