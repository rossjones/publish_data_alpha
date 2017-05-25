import uuid

from django.test import TestCase
from django.urls import reverse

from runtime_config.models import ConfigProperty
from runtime_config.logic import get_config


class ConfigTestCase(TestCase):

    def setUp(self):
        c1 = ConfigProperty.objects.create(
            key='ckan',
            value='https://test.data.gov.uk',
            active=False
        )
        c2 = ConfigProperty.objects.create(
            key='logserver',
            value='https://logging',
            active=True
        )

    def test_find_active(self):
        assert get_config('logserver') == 'https://logging'

    def test_find_inactive(self):
        assert get_config('ckan') is None

    def test_missing(self):
        assert get_config('missing') is None
