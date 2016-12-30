from django.test import TestCase
from django.contrib.auth import get_user_model

from ckan_proxy.logic import datasets_for_user
from ckan_proxy.util import test_user_key


class DatasetsTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username="Test User",
            apikey=test_user_key()
        )

    def test_datasets_for_user(self):
        def get_datasets(offset=0, limit=10):
            datasets = datasets_for_user(
                self.test_user,
                offset=offset,
                limit=limit
            )

            assert datasets['count'] > 0
            assert len(datasets['results']) == 1
            return datasets

        datasets = get_datasets(0, 10)
        if datasets['count'] > 10:
            second_page = get_datasets(10, 10)
            assert datasets['results'][0].get('id') != \
                second_page['results'][0].get('id')
