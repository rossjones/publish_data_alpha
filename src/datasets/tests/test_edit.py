import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset


class DatasetEditTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="Test User Signin",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

        # Log the user in
        self.client.post(reverse('signin'), {
            "email": "test-signin@localhost",
            "password": "password"
        })

        # Both test the initial dataset creation, and get a name we can
        # use for the remaining tests.
        self.dataset_name = self._create_new_dataset()


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
        assert r.status_code == 404

    def test_edit_get(self):
        r = self._edit_dataset(self.dataset_name)
        assert r.status_code == 200
        assert b'A test dataset for edit' in r.content


    def test_edit_update(self):
        response = self.client.post(
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

        ds = Dataset.objects.get(name=self.dataset_name)

