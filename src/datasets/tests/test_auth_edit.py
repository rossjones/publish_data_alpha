import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset


class DatasetAuthEditTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="test-signin@localhost",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

        # Log the user in
        self.client.login(username='test-signin@localhost', password='password')
        self.dataset_name = self._create_new_dataset()
        self.client.logout()

        self.random_user = get_user_model().objects.create(
            email="random_user@localhost",
            username="random_user@localhost",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()
        self.client.login(username='random_user@localhost', password='password')


    def _create_new_dataset(self):
        response = self.client.post(reverse('new_dataset', args=[]), {
                'title': 'A test dataset for edit',
                'description': 'A test description',
                'summary': 'A test summary',
        })
        assert response.status_code == 302
        parts = response.url.split('/')

        return parts[2]

    def _edit_dataset(self, name=None):
        response = self.client.get(
            reverse('edit_full_dataset',
            args=[name or self.dataset_name]))
        return response

    def test_bad_doesnotexist(self):
        r = self._edit_dataset('nope')
        assert r.status_code == 302, r.status_code
        assert r.url == reverse('signin') + "?next=/dataset/edit/nope"

    def test_edit_get(self):
        r = self._edit_dataset(self.dataset_name)
        assert r.status_code == 302
        assert r.url == reverse('signin') + "?next=/dataset/edit/" + self.dataset_name

    def test_edit_update(self):
        r = self.client.post(
            reverse('edit_full_dataset',
            args=[self.dataset_name]),
            {
                'name': self.dataset_name,
                'title': 'A test dataset for edit',
                'description': 'A test description',
                'summary': 'Updated summary',
                'licence': 'uk-ogl',
                'notifications': 'no'
            })

        assert r.status_code == 302

