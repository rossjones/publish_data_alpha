from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ckan_proxy.util import test_user_key


class SigninTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="Test User Signin",
            apikey=test_user_key()
        )
        self.test_user.set_password("password")
        self.test_user.save()

    def test_signin(self):
        response = self.client.post(reverse('signin'), {
            "email": "test-signin@localhost",
            "password": "password"
        })
        assert response.status_code == 302
        assert response.url == '/'

    def test_signin_fail(self):
        response = self.client.post(reverse('signin'), {
            "email": "no",
            "password": "nope"
        })
        assert response.status_code == 200
        assert 'There was a problem signing you in' in str(response.content)

    def test_signin_empty(self):
        response = self.client.post(reverse('signin'), {
            "email": "",
            "password": ""
        })
        assert response.status_code == 200
        # Assert error message on page
