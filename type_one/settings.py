SECRET_KEY = 'key'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'type_one.core'
    ]

AUTH_USER_MODEL = "core.User"

ROOT_URLCONF = "type_one.urls"