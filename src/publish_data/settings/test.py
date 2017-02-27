from .base import *


ES_INDEX = 'data_discovery_test'

# Speed up logins during testing/dev
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
