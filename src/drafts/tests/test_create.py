from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from drafts.models import Dataset

from ckan_proxy.util import test_user_key


def get_wizard_data(data, name):
    tmp = data
    tmp.update({"dataset_wizard-current_step": name})
    return tmp


class DraftsTestCase(TestCase):

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
                'summary': 'A test summary'
        })
        assert response.status_code == 302
        parts = response.url.split('/')
        return parts[2]

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
        u = reverse('edit_dataset_step', args=[self.dataset_name, 'country'])
        response = self.client.get(u)
        assert response.status_code == 200

        # No selected countries
        response = self.client.post(u, get_wizard_data({}, 'country'))
        assert response.status_code == 200
        assert self._get_dataset().countries == '[]'

        response = self.client.post(
            u,
            get_wizard_data({'country-countries': 'england'}, 'country')
        )
        assert response.status_code == 302
        assert self._get_dataset().countries == "['england']", \
            self._get_dataset().countries

    def test_licence(self):
        u = reverse('edit_dataset_step', args=[self.dataset_name, 'licence'])
        response = self.client.get(u)
        assert response.status_code == 200

        # No selected countries, expect a fail
        response = self.client.post(u, get_wizard_data({}, "licence"))
        assert response.status_code == 200

        response = self.client.post(
            u,
            get_wizard_data({'licence-licence': 'ogl'}, 'licence')
        )
        assert response.status_code == 302
        assert self._get_dataset().licence == "ogl", \
            self._get_dataset().licence

        response = self.client.post(
            u,
            get_wizard_data({
                'licence-licence': 'other',
                'licence-licence_other': 'pretend licence'
            }, 'licence')
        )
        assert response.status_code == 302
        obj = self._get_dataset()
        assert obj.licence == "other", obj.licence
        assert obj.licence_other == "pretend licence"

    def test_frequency(self):
        u = reverse('edit_dataset_step', args=[self.dataset_name, 'frequency'])
        response = self.client.get(u)
        assert response.status_code == 200

        response = self.client.post(u, get_wizard_data({}, 'frequency'))
        assert response.status_code == 200

        response = self.client.post(
            u,
            get_wizard_data({'frequency-frequency': 'never'}, 'frequency')
        )
        assert response.status_code == 302
        assert self._get_dataset().frequency == "never", \
            self._get_dataset().frequency

    def test_organisation(self):
        u = reverse(
            'edit_dataset_step',
            args=[self.dataset_name, 'organisation']
        )
        response = self.client.get(u)
        assert response.status_code == 200

        response = self.client.post(u, get_wizard_data({}, 'organisation'))
        assert response.status_code == 200

        response = self.client.post(
            u,
            get_wizard_data({
                'organisation-organisation': 'cabinet-office'
            }, 'organisation')
        )
        assert response.status_code == 302
        assert self._get_dataset().organisation == "cabinet-office", \
            self._get_dataset().organisation

    """
    def test_frequency_details(self):
        u = reverse('edit_dataset_step', args=[self.dataset_name, 'frequency'])
        response = self.client.post(
            u,
            get_wizard_data({'frequency-frequency': 'weekly'}, 'frequency')
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_frequency_weekly',
            args=[self.dataset_name, 'frequency_weekly'])

        response = self.client.post(
            u,
            get_wizard_data({'frequency-frequency': 'monthly'}, 'frequency')
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_step',
            args=[self.dataset_name, 'frequency_monthly'])

        response = self.client.post(
            u,
            get_wizard_data({'frequency-frequency': 'quarterly'}, 'frequency')
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_step',
            args=[self.dataset_name, 'frequency_quarterly'])

        response = self.client.post(
            u,
            get_wizard_data({'frequency-frequency': 'annually'}, 'frequency')
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_step',
            args=[self.dataset_name, 'frequency_annually'])

        response = self.client.post(
            u,
            get_wizard_data({
                'frequency-frequency': 'financial-year'
            }, 'frequency')
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_step-year',
            args=[self.dataset_name, 'frequency_financial_year'])
    """

    def test_notifications(self):
        u = reverse(
            'edit_dataset_step',
            args=[self.dataset_name, 'notifications']
        )
        response = self.client.get(u)
        assert response.status_code == 200

        response = self.client.post(u, get_wizard_data({}, 'notifications'))
        assert response.status_code == 200

        response = self.client.post(
            u,
            get_wizard_data({
                'notifications-notifications': 'yes'
            }, 'notifications')
        )
        assert response.status_code == 302
        assert self._get_dataset().notifications == "yes", \
            self._get_dataset().notifications

    def test_check(self):
        u = reverse(
            'edit_dataset_step',
            args=[self.dataset_name, 'check_dataset']
        )
        response = self.client.get(u)
        assert response.status_code == 200

    def test_addfile(self):
        u = reverse(
            'edit_dataset_step',
            args=[self.dataset_name, 'addfile_daily']
        )
        response = self.client.get(u)
        assert response.status_code == 302

        # Must add a file
        response = self.client.post(u, get_wizard_data({}, 'addfile_daily'))
        assert response.status_code == 200

        response = self.client.post(
            u,
            get_wizard_data(
                {'add_file-url': 'http://data.gov.uk'},
                'addfile_daily'
            )
        )
        assert response.status_code == 200

        response = self.client.post(
            u,
            get_wizard_data({
                'add_file-title': 'Not really a file'
            }, 'addfile_daily')
        )
        assert response.status_code == 200

        response = self.client.post(u, get_wizard_data({
            'add_file-url': 'http://data.gov.uk',
            'add_file-title': 'Not really a file'
        }, 'addfile_daily'))
        assert response.status_code == 200

    def test_showfiles(self):
        u = reverse('edit_dataset_step', args=[self.dataset_name, 'files'])
        response = self.client.get(u)
        assert response.status_code == 200
