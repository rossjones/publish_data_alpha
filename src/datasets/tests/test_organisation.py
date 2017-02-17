import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from datasets.models import Organisation
from datasets.logic import organisations_for_user

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)

class OrganisationTestCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create()
        self.test_user.set_password("password")
        self.test_user.save()

        self.organisation = OrganisationFactory.create(name='one')
        self.organisation.users.add(self.test_user)

        self.organisation2 = OrganisationFactory.create(name='two')
        self.organisation2.users.add(self.test_user)

    def test_user_in_org(self):
        assert self.organisation.users.first() == self.test_user

    def test_orgs_for_user(self):
        organisations = organisations_for_user(self.test_user)
        assert len(organisations) == 2
        assert organisations[0] == self.organisation
        assert organisations[1] == self.organisation2

    def test_primary_organisation(self):
        organisation = self.test_user.primary_organisation()
        assert organisation.name == self.organisation.name, organisation.name
