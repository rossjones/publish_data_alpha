import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import ugettext as _
from datasets.models import Dataset, Organisation

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

class DatasetsTestCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create()
        self.test_user.set_password("password")
        self.test_user.save()
        self.organisation = OrganisationFactory.create()
        self.organisation.users.add(self.test_user)
        self.client.login(username=self.test_user.email, password='password')
        self.dataset = DatasetFactory.create(organisation_id=self.organisation.id)

    def _get_dataset(self):
        return Dataset.objects.get(name=self.dataset.name)

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

    def test_location(self):
        u = reverse('edit_dataset_location', args=[self.dataset.name])
        response = self.client.get(u)
        assert response.status_code == 200

        # No selected countries
        response = self.client.post(u, {})
        assert response.status_code == 200

        ds = self._get_dataset()
        assert ds.location1 == ''
        assert ds.location2 == ''
        assert ds.location3 == ''

        response = self.client.post(
            u,
            {'location1': 'England, Wales'}
        )
        assert response.status_code == 302
        assert self._get_dataset().location1 == "England, Wales", \
            self._get_dataset().location1

    def test_licence(self):
        u = reverse('edit_dataset_licence', args=[self.dataset.name])
        response = self.client.get(u)
        assert response.status_code == 200

        # No selected licence, expect a fail
        response = self.client.post(u, {})
        assert response.status_code == 200

        response = self.client.post(
            u,
            {'licence': 'ogl'}
        )
        assert response.status_code == 302
        assert self._get_dataset().licence == "ogl", \
            self._get_dataset().licence

        # No other licence specified
        response = self.client.post(
            u,
            {
                'licence': 'other',
                'licence_other': ''
            }
        )
        self.assertContains(
            response,
            _('Please type the name of your licence'),
            2, 200
        )

        # Correct other licence
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
        u = reverse('edit_dataset_frequency', args=[self.dataset.name])
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

    # def test_organisation(self):
    #     u = reverse(
    #         'edit_dataset_organisation',
    #         args=[self.dataset.name]
    #     )
    #     # With only a single organisation, we expect a redirect
    #     response = self.client.get(u)
    #     assert response.status_code == 302, response.content

    #     # User in a single organisation so will be redirected
    #     response = self.client.post(u, {})
    #     assert response.status_code == 302

    #     response = self.client.post(
    #         u,
    #         {
    #             'organisation': self.organisation.id
    #         }
    #     )
    #     assert response.status_code == 302
    #     assert self._get_dataset().organisation.id == self.organisation.id

    def test_redirect_adding_extra_file(self):
        u = reverse('edit_dataset_files', args=[self.dataset.name])
        response = self.client.get(u)
        assert response.status_code == 200
        assert '/dataset/{}/addfile_weekly'.format(self.dataset.name) in response.content.decode('utf-8')


    def test_frequency_details(self):
        u = reverse('edit_dataset_frequency', args=[self.dataset.name])
        response = self.client.post(
            u,
            {'frequency': 'weekly'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_weekly',
            args=[self.dataset.name])

        response = self.client.post(
            u,
            {'frequency': 'monthly'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_monthly',
            args=[self.dataset.name])

        response = self.client.post(
            u,
            {'frequency': 'quarterly'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_quarterly',
            args=[self.dataset.name])

        response = self.client.post(
            u,
            {'frequency': 'annually'}
        )
        assert response.status_code == 302
        assert response.url == reverse('edit_dataset_addfile_annually',
            args=[self.dataset.name])

        #response = self.client.post(
        #    u,
        #    get_wizard_data({
        #        'frequency-frequency': 'financial-year'
        #    }, 'frequency')
        #)
        #assert response.status_code == 302
        #assert response.url == reverse('edit_dataset_step-year',
        #    args=[self.dataset.name, 'frequency_financial_year'])

    def test_adddoc(self):
        u = reverse(
            'edit_dataset_adddoc',
            args=[self.dataset.name]
        )
        response = self.client.get(u)
        assert response.status_code == 200, response.status_code

        # Assert an error
        response = self.client.post(u, {})
        assert response.status_code == 200, response.status_code

        response = self.client.post(
            u,
            {
                'name': 'A title',
                'url': 'https://data.gov.uk'
            }
        )
        assert response.status_code == 302
        assert response.url == reverse(
            'edit_dataset_documents',
            args=[self.dataset.name]
        )

    def test_check(self):
        u = reverse(
            'publish_dataset',
            args=[self.dataset.name]
        )
        response = self.client.get(u)
        assert response.status_code == 200

    def test_addfile(self):
        u = reverse(
            'edit_dataset_addfile_weekly',
            args=[self.dataset.name]
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
        u = reverse('edit_dataset_files', args=[self.dataset.name])
        response = self.client.get(u)
        assert response.status_code == 200

    def test_publish_page_add_change(self):
        ''' Check that when no location is specified the publish
        screen says 'Add' and when there is a location it says
        'Change'.
        '''
        u = reverse('publish_dataset', args=[self.dataset.name])
        self.assertContains(
            self.client.get(u),
            'Add <span class=\'visuallyhidden\'>location</span>',
            1, 200
        )
        u = reverse(
            'edit_dataset_location',
            args=[self.dataset.name]
        )
        self.client.post(u, {'location1': 'Paris'}),
        u = reverse('publish_dataset', args=[self.dataset.name])
        self.assertContains(
            self.client.get(u),
            'Change <span class=\'visuallyhidden\'>location</span>',
            1, 200
        )
