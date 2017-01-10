from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset

from ckan_proxy.util import test_user_key


class DatasetsTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="Test User Signin",
            apikey=test_user_key()
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

    def test_bad_slug(self):
        response = self.client.post(reverse('new_dataset', args=[]), {
                'title': '[]',
                'description': 'A test description',
                'summary': 'A test summary'
        })
        assert response.status_code == 200

    def test_missing_summary(self):
        response = self.client.post(reverse('new_dataset', args=[]), {
                'title': '[]',
                'description': 'A test description'
        })
        assert response.status_code == 200

    def test_country(self):
        u = reverse('edit_dataset_country', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 200

        # No selected countries
        response = self.client.post(u, {})
        assert response.status_code == 200
        assert self._get_dataset().countries == '[]'

        response = self.client.post(
            u,
            {'countries': 'england'}
        )
        assert response.status_code == 302
        assert self._get_dataset().countries == "['england']", \
            self._get_dataset().countries

    def test_licence(self):
        u = reverse('edit_dataset_licence', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 200

        # No selected countries, expect a fail
        response = self.client.post(u, {})
        assert response.status_code == 200

        response = self.client.post(
            u,
            {'licence': 'ogl'}
        )
        assert response.status_code == 302
        assert self._get_dataset().licence == "ogl", \
            self._get_dataset().licence

        response = self.client.post(
            u,
            {
                'licence': 'other',
                'licence_other': 'pretend licence'
            }
        )
        assert response.status_code == 302
        obj = self._get_dataset()
        assert obj.licence == "other", obj.licence
        assert obj.licence_other == "pretend licence"

    def test_frequency(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 200

        response = self.client.post(u, {})
        assert response.status_code == 200

        response = self.client.post(
            u,
            {'frequency': 'never'}
        )
        assert response.status_code == 302
        assert self._get_dataset().frequency == "never", \
            self._get_dataset().frequency

    def test_organisation(self):
        u = reverse(
            'edit_dataset_organisation',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 200

        response = self.client.post(u, {})
        assert response.status_code == 200

        response = self.client.post(
            u,
            {
                'organisation': 'cabinet-office'
            }
        )
        assert response.status_code == 302
        assert self._get_dataset().organisation == "cabinet-office", \
            self._get_dataset().organisation


    def test_redirect_adding_extra_file(self):
        u = reverse('edit_dataset_files', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 200
        assert '/dataset/{}/addfile_weekly'.format(self.dataset_name) in response.content.decode('utf-8')


    def test_frequency_details(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset_name])
        response = self.client.post(
            u,
            {'frequency': 'weekly'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_weekly',
            args=[self.dataset_name])

        response = self.client.post(
            u,
            {'frequency': 'monthly'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_monthly',
            args=[self.dataset_name])

        response = self.client.post(
            u,
            {'frequency': 'quarterly'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_quarterly',
            args=[self.dataset_name])

        response = self.client.post(
            u,
            {'frequency': 'annually'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_annually',
            args=[self.dataset_name])

        #response = self.client.post(
        #    u,
        #    get_wizard_data({
        #        'frequency-frequency': 'financial-year'
        #    }, 'frequency')
        #)
        #assert response.status_code == 302
        #assert response.url == reverse('edit_dataset_step-year',
        #    args=[self.dataset_name, 'frequency_financial_year'])

    def test_notifications(self):
        u = reverse(
            'edit_dataset_notifications',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 200

        response = self.client.post(u, {})
        assert response.status_code == 200

        response = self.client.post(
            u,
            {
                'notifications': 'yes'
            }
        )
        assert response.status_code == 302
        assert self._get_dataset().notifications == "yes", \
            self._get_dataset().notifications

    def test_check(self):
        u = reverse(
            'edit_dataset_check_dataset',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 200

    def test_addfile(self):
        u = reverse(
            'edit_dataset_addfile_weekly',
            args=[self.dataset_name]
        )
        response = self.client.get(u)
        assert response.status_code == 200

        # Must add a file, and this fails
        response = self.client.post(u, {})
        assert response.status_code == 200

        response = self.client.post(
            u,
            {'url': 'http://data.gov.uk'},
        )
        assert response.status_code == 200

        response = self.client.post(
            u,
            {
                'title': 'Not really a file'
            }
        )
        assert response.status_code == 200

        response = self.client.post(u, {
            'url': 'http://data.gov.uk',
            'title': 'Not really a file'
        })
        assert response.status_code == 200

    def test_showfiles(self):
        u = reverse('edit_dataset_files', args=[self.dataset_name])
        response = self.client.get(u)
        assert response.status_code == 200
