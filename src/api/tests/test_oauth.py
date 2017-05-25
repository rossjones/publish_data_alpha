import os
import uuid
from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .util import new_app_and_token

TOKEN = 'tokenstring'


class AuthorisationTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="test-signin@localhost",
            apikey=str(uuid.uuid4())
        )

        self.app, self.access_token = new_app_and_token(self.test_user, TOKEN)

    def test_forbidden_no_token(self):
        res = self.client.get('/api/status')
        assert res.status_code == 403

    def test_success_with_token(self):
        res = self.client.get('/api/status',
                              HTTP_AUTHORIZATION='Bearer {}'.format(TOKEN))
        assert res.status_code == 200
        assert res.content.decode()[0] == '{'
