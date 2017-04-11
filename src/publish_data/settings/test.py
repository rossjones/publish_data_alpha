from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

USE_TZ = True

ES_INDEX = 'data_discovery_test'

# Disable papertrail during tests
AUDIT = False

# Speed up logins during testing/dev
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
