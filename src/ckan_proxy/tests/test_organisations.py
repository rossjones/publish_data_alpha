from django.test import TestCase
from django.contrib.auth import get_user_model

from ckan_proxy.logic import organization_list, organization_list_for_user
from ckan_proxy.util import test_user_key

class OrganisationTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username="Test User",
            apikey=test_user_key()
        )

    def test_organisation_list(self):
        publishers = organization_list()
        assert len(publishers) > 1000

    def test_user_organisation_list(self):
        publishers = organization_list_for_user(self.test_user)
        assert len(publishers) > 0
