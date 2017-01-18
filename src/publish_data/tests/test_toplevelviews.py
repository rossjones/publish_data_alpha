import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class TopLevelViewsCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="Test User Signin",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

    def test_homepage_is_startpage(self):
        response = self.client.get('/')
        assert 'You must create an account to use this service' in \
            str(response.content)

    def test_homepage_is_dashboard_when_logged_in(self):
        response = self.client.post('/accounts/signin', {
            'email': self.test_user.email,
            'password': 'password'
        })
        assert response.status_code == 302
        assert response.url == '/'

        response = self.client.get('/')
        assert 'Dashboard' in str(response.content)

    def test_manage_redirects(self):
        response = self.client.get(reverse('manage_data'))
        assert response.status_code == 302
        assert response.url == '/accounts/signin?next=/manage'

    def test_manage_ok_when_logged_in(self):
        response = self.client.post('/accounts/signin', {
            'email': self.test_user.email,
            'password': 'password'
        })
        assert response.status_code == 302
        assert response.url == '/'

        response = self.client.get('/manage')
        assert response.status_code == 200
        assert 'Manage data' in str(response.content)
