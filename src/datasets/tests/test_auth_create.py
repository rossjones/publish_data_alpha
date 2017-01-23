import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset, Organisation



class DatasetsCreateAuthTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="test-signin@localhost",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

        self.organisation = Organisation.objects.create(
            name='test-org',
            title='Test Organisation',
            description='Test Organisation Description'
        )
        self.organisation.users.add(self.test_user)

        self.client.login(username='test-signin@localhost', password='password')
        self.dataset_name = self._create_new_dataset()
        self.client.logout()

        self.random_user = get_user_model().objects.create(
            email="random_user@localhost",
            username="test-random_user@localhost",
            apikey=str(uuid.uuid4())
        )
        self.random_user.set_password("password")
        self.random_user.save()
        self.client.login(username='random_user@localhost', password='password')

    def _create_new_dataset(self):
        response = self.client.post(reverse('new_dataset', args=[]), {
                'title': 'A test dataset for create',
                'description': 'A test description',
                'summary': 'A test summary',
        })
        assert response.status_code == 302

        parts = response.url.split('/')
        name = parts[2]

        # Set frequency
        response = self.client.post(reverse('edit_dataset_frequency', args=[name]), {
                'frequency': 'weekly',
        })
        assert response.status_code == 302

        return name

    def _get_dataset(self):
        return Dataset.objects.get(name=self.dataset_name)

    def test_location(self):
        u = reverse('edit_dataset_location', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 403

        # No selected countries
        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'location': 'England, Wales'}
        )
        assert response.status_code == 403

    def test_licence(self):
        u = reverse('edit_dataset_licence', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 403

        # No selected countries, expect a fail
        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'licence': 'ogl'}
        )
        assert response.status_code == 403

        response = self.client.post(
            u,
            {
                'licence': 'other',
                'licence_other': 'pretend licence'
            }
        )
        assert response.status_code == 403
        obj = self._get_dataset()
        assert obj.licence == ""
        assert obj.licence_other == ""

    def test_frequency(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 403

        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'frequency': 'never'}
        )
        assert response.status_code == 403


    def test_organisation(self):
        u = reverse(
            'edit_dataset_organisation',
            args=[self.dataset_name]
        )
        # With only a single organisation, we expect a redirect
        response = self.client.get(u)
        assert response.status_code == 403, response.content

        # User in a single organisation so will be redirected
        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {
                'organisation': self.organisation.id
            }
        )
        assert response.status_code == 403


    def test_redirect_adding_extra_file(self):
        u = reverse('edit_dataset_files', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 403

    def test_frequency_details(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset_name])
        response = self.client.post(
            u,
            {'frequency': 'weekly'}
        )
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'frequency': 'monthly'}
        )
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'frequency': 'quarterly'}
        )
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'frequency': 'annually'}
        )
        assert response.status_code == 403

    def test_adddoc(self):
        u = reverse(
            'edit_dataset_adddoc',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 403

        # Assert an error
        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {
                'title': 'A title',
                'url': 'https://data.gov.uk'
            }
        )
        assert response.status_code == 403

    def test_notifications(self):
        u = reverse(
            'edit_dataset_notifications',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 403

        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {
                'notifications': 'yes'
            }
        )
        assert response.status_code == 403


    def test_check(self):
        u = reverse(
            'edit_dataset_check_dataset',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 403


    def test_addfile(self):
        u = reverse(
            'edit_dataset_addfile_weekly',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 403

        # Must add a file, and this fails
        response = self.client.post(u, {})
        assert response.status_code == 403

        response = self.client.post(
            u,
            {'url': 'http://data.gov.uk'},
        )
        assert response.status_code == 403

        response = self.client.post(
            u,
            {
                'title': 'Not really a file'
            }
        )
        assert response.status_code == 403

        response = self.client.post(u, {
            'url': 'http://data.gov.uk',
            'title': 'Not really a file'
        })
        assert response.status_code == 403


    def test_showfiles(self):
        u = reverse('edit_dataset_files', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 403, response.status_code
