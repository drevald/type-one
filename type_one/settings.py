import os
import environ

env = environ.Env()

#BASE_DIR = '/home/denis/PythonProjects/type-one/type_one/'

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
    'django.contrib.staticfiles',
    'bootstrap4',
    'type_one.core',
    'type_one.records',
    'type_one.ingredients',
    'django_extensions',
    'debug_toolbar'
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
    'django.middleware.locale.LocaleMiddleware'
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
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'type_one',
    #     'USER': 'postgres',
    #     'PASSWORD': 'password',
    #     'HOST': 'postgres',
    #     'PORT': '5432',
    # }    
}

STATIC_URL = '/static/'

SECRET_KEY = 'segretto'

DEBUG = True

AUTH_USER_MODEL = "core.User"

SESSION_SAVE_EVERY_REQUEST = True

ALLOWED_HOSTS = [
    '192.168.0.189',
    '127.0.0.1',
    'localhost',
    'type-one.herokuapp.com'
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOCALE_PATHS = ( 
    os.path.join(str(BASE_DIR), "locale"),
)