from django.utils.translation import ugettext as _
from calendar import monthrange
from datetime import datetime
from mimetypes import guess_extension
from urllib.parse import urlparse

from django.utils.text import slugify

import requests


def url_exists(url):
    ''' Checks whether the provided URL is valid, and returns
    a tuple containing:
        a bool - for success/fail
        a string - the determined format (may be None)
        an integer - the size of the resource
        a string - an error message
    '''
    # Make sure we have a valid proto,
    obj = urlparse(url)
    if not obj.scheme.lower() in ['http', 'https', 'ftp', 'ftps']:
        return False, '', 0,  _('The URL should begin with http or https')

    fmt = ''
    size = 0

    try:
        r = requests.head(url, allow_redirects=True)
    except requests.ConnectionError as ce:
        return False, '', 0, _('Failed to connect to the URL')
    except Exception as e:
        return False, '', 0, _('A problem occurred checking the URL')

    if r.status_code != 200:
        return False, '', 0, _('The URL caused an error')

    content_type = r.headers['Content-Type']

    if ';' in content_type:
        # TODO: Let's not through away encoding information
        content_type = content_type[0:content_type.index(';')]

    if 'Content-Length' in r.headers:
        size = int(r.headers['Content-Length'])

    extension = guess_extension(content_type)
    if extension:
        fmt = extension[1:].upper()
        # Mimetypes vary and so there's not an obviously easy way
        # to get the extension we want for some types. Notably
        # HTML/SHTML
        if fmt in ['HTM', 'SHTML']:
            fmt = 'HTML'

    return True, fmt, size, None


def calculate_dates_for_month(month, year):
    (_, e,) = monthrange(year, month)
    return (
        datetime(year=year, month=month, day=1),
        datetime(year=year, month=month, day=e)
    )


def calculate_dates_for_quarter(q, year=2017):
    first_month_of_quarter = 3 * q - 2
    last_month_of_quarter = 3 * q
    sd, _ = calculate_dates_for_month(first_month_of_quarter, year)
    _, ed = calculate_dates_for_month(last_month_of_quarter, year)
    return (sd, ed,)


def calculate_dates_for_year(year):
    return (
        datetime(year=year, month=1, day=1),
        datetime(year=year, month=12, day=31)
    )


