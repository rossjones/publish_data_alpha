from django.conf import settings

import papertrail


def audit_log(*args, **kwargs):
    if settings.AUDIT:
        papertrail.log(*args, **kwargs)
