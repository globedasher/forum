from .base import *

print("Running in Dev Mode")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

INSTALLED_APPS += [
        'debug_toolbar',
        ]

# This will cause any email activity from django to be captured in the log
# files and blocks sending. Keep here and comment out if needed for testing.
#EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
#EMAIL_FILE_PATH = 'tmp/email' # change this to a proper location

MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        ]


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
