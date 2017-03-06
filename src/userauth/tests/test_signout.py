import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse



class SignoutTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signout@localhost",
            username="Test User Signin",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

    def test_signin_and_then_out(self):
        response = self.client.post(reverse('signin'), {
            "email": "test-signout@localhost",
            "password": "password"
        })
        assert response.status_code == 302
        assert response.url == '/tasks'

        response = self.client.post(reverse('signout'), {})
        assert response.status_code == 302
        assert response.url == '/'

    def test_non_signedin_signout(self):
        response = self.client.post(reverse('signout'), {})
        assert response.status_code == 302
        assert response.url == '/'
