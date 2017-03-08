import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)


class DatasetAuthEditTestCase(TestCase):

    def setUp(self):
        self.dataset = DatasetFactory.create()

        self.random_user = NaughtyUserFactory.create()
        self.random_user.set_password("password")
        self.random_user.save()
        self.client.login(username=self.random_user.email, password='password')

    def _edit_dataset(self, name=None):
        response = self.client.get(
            reverse('edit_full_dataset',
            args=[name or self.dataset.name]))
        return response

    def test_bad_doesnotexist(self):
        r = self._edit_dataset('nope')
        assert r.status_code == 404, r.status_code

    def test_edit_get_fail(self):
        r = self._edit_dataset(self.dataset.name)
        assert r.status_code == 403, r.status_code

    def test_edit_update(self):
        r = self.client.post(
            reverse('edit_full_dataset',
            args=[self.dataset.name]),
            {
                'name': self.dataset.name,
                'title': 'A test dataset for edit',
                'description': 'A test description',
                'summary': 'Updated summary',
                'licence': 'uk-ogl'
            })

        assert r.status_code == 403
