from django.utils.translation import ugettext as _
from calendar import monthrange
from datetime import datetime
from mimetypes import guess_extension
from urllib.parse import urlparse

import os.path
import requests


class URLValidationResponse:
    def __init__(self, success=True, format='', size=0, error=None,
                 last_modified=None):
        self.success = success
        self.format = format
        self.size = size
        self.error = error
        self.last_modified = last_modified

    @classmethod
    def success(cls, format, size, last_modified):
        return cls(success=True, format=format, size=size,
                   last_modified=last_modified)

    @classmethod
    def error(cls, message):
        return cls(success=False, error=_(message))

    def __repr__(self):
        return (
            "<URLValidResponse: success={success}, format={format}, " +
            "size={size}, error={error}, last_modified={last_modified}>"
        ).format(self.__dict__)


def url_exists(url):
    ''' Checks whether the provided URL is valid, and returns
    a namedtuple (URLValidResponse) containing:
        a bool - for success/fail
        a string - the determined format (may be None)
        an integer - the size of the resource
        a string - an error message
        a datetime - the last modified time of the file
    '''

    # Make sure we have a valid proto,
    obj = urlparse(url)
    if not obj.scheme.lower() in ['http', 'https', 'ftp', 'ftps']:
        return False, '', 0, _('The URL should begin with http or https')

    fmt = ''
    size = 0

    try:
        r = requests.head(url, allow_redirects=True)
    except requests.ConnectionError:
        return URLValidationResponse.error('Failed to connect to the URL')
    except Exception:
        return URLValidationResponse.error('A problem occurred checking the URL')

    if r.status_code != 200:
        return URLValidationResponse.error('The URL caused an error')

    fmt = guess_file_format(url, r.headers)

    if 'Content-Length' in r.headers:
        size = int(r.headers['Content-Length'])

    return URLValidationResponse.success(fmt, size, None)


def guess_file_format(url, headers):
    """
    Try to figure out the format of the file, first from
    content-disposition, then url, then mime type
    """

    # We have a number of functions -> (url, header) that can
    # try to get a filetype out of the args in some way
    filetype_finders = [
        filetype_from_content_disposition,
        filetype_from_url,
        filetype_from_mime_type
    ]

    # Try each in turn. The first one that returns a non-blank string, we
    # return which breaks out of the whole function and skips the rest of
    # the loop... a little nicer that a cascade of many ifs
    for finder in filetype_finders:
        filetype = finder(url, headers)
        if filetype:
            return filetype.upper().strip('.')

    # Safe condition - no info could be found
    return ''


def filetype_from_content_disposition(_url, headers):
    content_disposition = headers.get('Content-Disposition')

    if content_disposition and 'filename=' in content_disposition:
        filename = content_disposition.split('filename=')[1]
        filename = filename.strip('"\'')
        file_ext = os.path.splitext(filename)[1]
        return file_ext

    return ''


def filetype_from_url(url, _headers):
    url_path = urlparse(url).path
    url_ext = os.path.splitext(url_path)[1]

    return url_ext


def filetype_from_mime_type(_url, headers):
    content_type = headers.get('Content-Type')

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

    return fmt


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
