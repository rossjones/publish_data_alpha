import os
import json
import uuid
from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .util import new_app_and_token

from datasets.tests.factories import (GoodUserFactory,
                                      NaughtyUserFactory,
                                      OrganisationFactory,
                                      DatasetFactory)

TOKEN = 'tokenstring'

class DatasetTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="test-signin@localhost",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()
        self.client.login(username=self.test_user.email, password='password')

        self.app, self.access_token = new_app_and_token(self.test_user, TOKEN)

        self.organisation = OrganisationFactory.create()
        self.organisation.users.add(self.test_user)
        self.dataset = DatasetFactory.create(
            organisation_id=self.organisation.id,
            name='my-test-dataset',
            title='My Test Dataset'
        )

    def test_successful_list(self):
        res = self.client.get('/api/1/datasets',
            HTTP_AUTHORIZATION='Bearer {}'.format(TOKEN))
        assert res.status_code == 200
        data = json.loads(res.content.decode('utf-8'))
        assert data['count'] >= 1


    def test_successful_create(self):
        dataset_dict = {
            'name': 'created-dataset',
            'title': 'Created dataset',
            'description': 'Dataset',
            'files': [{
                'url': 'http://localhost',
                'name': 'Test file'
            }]
        }
        res = self.client.post('/api/1/datasets',
            json.dumps(dataset_dict),
            content_type="application/json",
            HTTP_AUTHORIZATION='Bearer {}'.format(TOKEN))
        assert res.status_code == 201, res.status_code
        dataset = json.loads(res.content.decode('utf-8'))
        assert len(dataset['files']) == 1


    def test_successful_get(self):
        res = self.client.get('/api/1/datasets/{}'.format(self.dataset.name),
            HTTP_AUTHORIZATION='Bearer {}'.format(TOKEN))
        assert res.status_code == 200
        data = json.loads(res.content.decode('utf-8'))
        assert data['url'] == 'http://testserver/api/1/datasets/my-test-dataset'
