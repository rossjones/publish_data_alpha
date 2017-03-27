import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import ugettext as _
from datasets.models import Dataset

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

class DatasetEditTestCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory()
        self.test_user.set_password("password")
        self.test_user.save()

        success = self.client.login(username=self.test_user.email, password='password')

        self.dataset = DatasetFactory.create(creator=self.test_user)
        self.datafile = DatafileFactory.create(dataset=self.dataset)


    def _edit_dataset(self, name=None):
        response = self.client.get(
            reverse('edit_full_dataset',
            args=[name or self.dataset.name]))
        return response

    def test_bad_doesnotexist(self):
        r = self._edit_dataset('nope')
        assert r.status_code == 404

    def test_edit_get(self):
        r = self._edit_dataset(self.dataset.name)
        assert r.status_code == 200
        assert bytes(self.dataset.title, encoding='utf-8') in r.content


    def test_edit_update(self):
        response = self.client.post(
            reverse('edit_full_dataset',
            args=[self.dataset.name]),
            {
                'name': self.dataset.name,
                'title': 'A test dataset for edit',
                'description': 'A test description',
                'summary': 'Updated summary',
                'licence': 'uk-ogl'
            })

        ds = Dataset.objects.get(name=self.dataset.name)

    def test_delete_datafile(self):
        ''' Check datafile delete confirmation and final message '''

        # Confirm
        url = reverse(
            'edit_dataset_confirmdeletefile',
            args=[self.dataset.name, self.datafile.id]
        )
        response = self.client.post(url)
        self.assertContains(
            response,
            _('Are you sure you want to delete ‘{}’?'.format(
                self.datafile.title)
            ),
            1, 200
        )

        # Delete
        url = reverse(
            'edit_dataset_deletefile',
            args=[self.dataset.name, self.datafile.id]
        )
        response = self.client.post(url, follow=True)
        self.assertContains(
            response,
            _('Your link ‘{}’ has been deleted'.format(self.datafile.title)),
            1, 200
        )


    def test_delete_dataset(self):
        ''' Check dataset delete confirmation and final message '''

        # Confirm
        url = reverse(
            'confirm_delete_dataset',
            args=[self.dataset.name]
        )
        response = self.client.post(url)
        self.assertContains(
            response,
            _('Are you sure you want to delete this dataset?'),
            1, 200
        )

        # Delete
        url = reverse(
            'delete_dataset',
            args=[self.dataset.name]
        )
        response = self.client.get(url, follow=True)
        self.assertContains(
            response,
            _('The dataset ‘{}’ has been deleted'.format(self.dataset.title)),
            1, 200
        )
