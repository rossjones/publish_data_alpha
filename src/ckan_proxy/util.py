import os

from django.conf import settings

from ckanapi import RemoteCKAN


CKAN_CONNECTION = None


def get_ckan_host():
    """ Load the CKAN host either from settings, or if not from
        Environment """
    if not hasattr(settings, "CKAN_HOST"):
        return os.environ.get("CKAN_HOST")
    return settings.CKAN_HOST


def get_ckan_admin():
    """ Load the CKAN Admin API Key from settings or from
        Environment """
    if not hasattr(settings, "CKAN_ADMIN"):
        return os.environ.get("CKAN_ADMIN")
    return settings.CKAN_ADMIN


def ckan_connection_for_admin():
    """ Returns a CKAN connection for the admin user """
    global CKAN_CONNECTION
    if not CKAN_CONNECTION:
        CKAN_CONNECTION = RemoteCKAN(
            get_ckan_host(),
            apikey=get_ckan_admin()
        )
    return CKAN_CONNECTION


def ckan_connection_for_user(apikey):
    """ Returns a CKAN connection for the specified key """
    return RemoteCKAN(get_ckan_host(), apikey=apikey)


def test_user_key():
    """ The API Key of a test user """
    if not hasattr(settings, "CKAN_TEST_USER"):
        return os.environ.get("CKAN_TEST_USER")
    return settings.CKAN_TEST_USER
