from .base import *

DEBUG = False

STATIC_ROOT = os.path.join(PROJECT_DIR, 'staticfiles')
STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "assets/govuk_template/static"),
    os.path.join(PROJECT_DIR, "assets"),
]
