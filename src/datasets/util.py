from calendar import monthrange
from datetime import datetime
from mimetypes import guess_extension

from django.utils.text import slugify

import requests


def url_exists(url):
    fmt = ''

    try:
        r = requests.head(url, allow_redirects=True)
    except requests.ConnectionError as ce:
        return False, ''
    except Exception as e:
        return False, ''

    content_type = r.headers['Content-Type']

    if ';' in content_type:
        # TODO: Let's not through away encoding information
        content_type = content_type[0:content_type.index(';')]

    extension = guess_extension(content_type)
    if extension:
        fmt = extension[1:].upper()
        # Mimetypes vary and so there's not an obviously easy way
        # to get the extension we want for some types. Notably
        # HTML/SHTML
        if fmt in ['HTM', 'SHTML']:
            fmt = 'HTML'

    return True, fmt


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


