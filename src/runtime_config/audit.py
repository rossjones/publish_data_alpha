from django.conf import settings

import papertrail


def audit_log(*args, **kwargs):
    if settings.AUDIT == True:
        papertrail.log(*args, **kwargs)
