from django.test import TestCase

from datasets.util import url_exists


class MiscTestCase(TestCase):


    def test_url_exists_ok(self):
        exists, fmt, error = url_exists('https://data.gov.uk')
        assert exists
        assert fmt == 'HTML', fmt
        assert not error

    def test_url_exists_csv(self):
        exists, fmt, error = url_exists(
            'https://data.gov.uk/data/site-usage/data_all.csv'
        )
        assert exists
        assert fmt == 'CSV', fmt
        assert not error

    def test_url_does_not_exist(self):
        exists, fmt, error = url_exists('https://12345.12345.12345.org')
        assert not exists
        assert fmt == ''
        assert 'Failed to connect' in error

    def test_url_missing_proto(self):
        exists, fmt, error = url_exists('data.gov.uk')
        assert not exists
        assert fmt == ''
        assert 'https' in error
