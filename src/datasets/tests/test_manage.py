import re
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset, Organisation

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

class ManageTestCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create(username='bob', email='bob@localhost')
        self.test_user.set_password("password")
        self.test_user.save()
        self.test_user2 = GoodUserFactory.create(username='bleh',email='bleh@localhost')
        self.test_user2.set_password("password")
        self.test_user2.save()

        self.organisation = OrganisationFactory.create()
        self.organisation.users.add(self.test_user)
        self.organisation.users.add(self.test_user2)

        self.client.login(username=self.test_user.email, password='password')
        self.dataset_a = DatasetFactory.create(
            organisation_id=self.organisation.id,
            name='a-dataset',
            title='A dataset'
        )
        self.dataset_b = DatasetFactory.create(
            organisation_id=self.organisation.id,
            name='b-dataset',
            title='B dataset'
        )


    def test_manage_sorting(self):
        ''' Check sorting order types '''
        manage_page = self.client.get(reverse('manage_org_data'))
        self.assertContains(
            manage_page,
            '<span>Manage your datasets</span>',
            1, 200, html=True
        )
        assert re.match(r'.*B dataset.+A dataset.*', str(manage_page.content))
        manage_page = self.client.get(reverse('manage_org_data')+'?sort=name')
        assert re.match(r'.*A dataset.+B dataset.*', str(manage_page.content))
        manage_page = self.client.get(reverse('manage_org_data')+'?sort=-name')
        assert re.match(r'.*B dataset.+A dataset.*', str(manage_page.content))


    def test_manage_tabs(self):

        dataset_c = DatasetFactory.create(
            organisation_id = str(self.organisation.id),
            name='c-dataset',
            title='C dataset',
            creator=self.test_user2,
            owner=self.test_user2
        )

        self.client.login(username=self.test_user2.email, password='password')

        # self.test_user's own datasets are self.dataset_c
        response = self.client.get(reverse('manage_my_data'))
        self.assertContains(response, 'C dataset', 3, 200)
        self.assertNotContains(response, 'B dataset', status_code = 200)
        self.assertNotContains(response, 'A dataset', status_code = 200)

        # self.test_user's org datasets are self.dataset_a|b|c
        response = self.client.get(reverse('manage_org_data'))
        self.assertContains(response, 'C dataset', 3, 200)
        self.assertContains(response, 'B dataset', 3, 200)
        self.assertContains(response, 'A dataset', 3, 200)
