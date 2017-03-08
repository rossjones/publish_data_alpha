import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset, Organisation

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)


class DatasetsCreateAuthTestCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create()
        self.test_user.set_password("password")
        self.test_user.save()

        self.organisation = OrganisationFactory.create()
        self.organisation.users.add(self.test_user)

        self.client.login(username='test-signin@localhost', password='password')
        self.dataset = DatasetFactory.create()
        self.client.logout()

        self.random_user = NaughtyUserFactory.create()
        self.random_user.set_password("password")
        self.random_user.save()
        self.client.login(username=self.random_user.email, password='password')


    def test_location(self):
        u = reverse('edit_dataset_location', args=[self.dataset.name])
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
        u = reverse('edit_dataset_licence', args=[self.dataset.name])
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
        assert self.dataset.licence == ""
        assert self.dataset.licence_other == ""

    def test_frequency(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset.name])
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
            args=[self.dataset.name]
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
        u = reverse('edit_dataset_files', args=[self.dataset.name])
        response = self.client.get(u)
        assert response.status_code == 403

    def test_frequency_details(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset.name])
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
            args=[self.dataset.name]
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

    def test_check(self):
        u = reverse(
            'publish_dataset',
            args=[self.dataset.name]
        )
        response = self.client.get(u)
        assert response.status_code == 403


    def test_addfile(self):
        u = reverse(
            'edit_dataset_addfile_weekly',
            args=[self.dataset.name]
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
        u = reverse('edit_dataset_files', args=[self.dataset.name])
        response = self.client.get(u)
        assert response.status_code == 403, response.status_code
