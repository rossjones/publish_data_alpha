from .base import *


# Speed up logins during testing/dev
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
