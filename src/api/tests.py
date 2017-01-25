import os
import uuid
from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from oauth2_provider.models import Application, AccessToken

TOKEN = 'tokenstring'

class OAuthTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="test-signin@localhost",
            apikey=str(uuid.uuid4())
        )
        self.app = Application.objects.create(
            user=self.test_user,
            redirect_uris='',
            client_type='confidential',
            authorization_grant_type='password',
            name='test app',
            skip_authorization=True
        )

        self.access_token = AccessToken.objects.create(
            user=self.test_user,
            token=TOKEN,
            application=self.app,
            expires=datetime.utcnow() + timedelta(days=1),
            scope='',
        )


    def test_forbidden_no_token(self):
        res = self.client.get('/api/status')
        assert res.status_code == 403

    def test_success_with_token(self):
        res = self.client.get('/api/status',
            HTTP_AUTHORIZATION='Bearer {}'.format(TOKEN))
        assert res.status_code == 200
        assert res.content.decode()[0] == '{'
