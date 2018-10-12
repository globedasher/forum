from .base import *

print("Running in Prod Mode")

ALLOWED_HOSTS = ['www.pureprune.com']

# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'heartbeat',
        'USER': 'platform',
        'PASSWORD': 'flatfruit',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Email settings
# https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-EMAIL_HOST
