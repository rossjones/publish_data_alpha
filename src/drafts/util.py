from calendar import monthrange
from datetime import datetime
from mimetypes import guess_extension

from django.utils.text import slugify

from drafts.models import Dataset
from ckan_proxy.logic import dataset_show

import requests


def url_exists(url):
    fmt = ''

    try:
        r = requests.head(url)
    except requests.ConnectionError as ce:
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


def calculate_dates_for_quarter(q, year):
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


def convert_to_slug(title):
    """ Checks for a local dataset with this name, and if not
    found also checks the CKAN install to make sure it isn't in use """
    t = title

    slug = None
    counter = 1

    while True:
        slug = slugify(t)
        if not slug:
            return None

        draft, dataset = None, None

        try:
            draft = Dataset.objects.get(name=slug)
        except Dataset.DoesNotExist:
            dataset = dataset_show(slug)

        if not draft and not dataset:
            break

        t = "{}{}".format(title, counter)
        counter += 1

    return slug
