from application.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SECRET_KEY = "ZZZ"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        # 'PASSWORD': DB_PASS,  # Not used with sqlite3.
        'HOST': 'db',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_ROOT = '/static_files/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/media_files/'
MEDIA_URL = '/media/'

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1'
]
