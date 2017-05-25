import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset, Organisation, Datafile
from datasets.auth import user_can_edit_dataset, user_can_edit_datafile

from .factories import (GoodUserFactory,
                        NaughtyUserFactory,
                        OrganisationFactory,
                        DatasetFactory,
                        DatafileFactory)


class AuthTestCase(TestCase):

    def setUp(self):
        self.test_user = GoodUserFactory.create()
        self.test_user.set_password("password")
        self.test_user.save()

        self.naughty_user = NaughtyUserFactory.create()

        self.organisation = Organisation.objects.create(
            name='test-org',
            title='Test Organisation',
            description='Test Organisation Description'
        )
        self.organisation.users.add(self.test_user)

        # Log the user in
        self.client.post(reverse('signin'), {
            "email": self.test_user.email,
            "password": "password"
        })

        # Both test the initial dataset creation, and get a name we can
        # use for the remaining tests.
        self.dataset = DatasetFactory.create()
        self.dataset.organisation = self.organisation
        self.dataset.save()

        self.datafile = DatafileFactory.create(dataset=self.dataset)

    def test_user_has_access(self):
        can = user_can_edit_dataset(self.test_user, self.dataset)
        assert can, can

    def test_user_has_file_access(self):
        can = user_can_edit_datafile(self.test_user, self.datafile)
        assert can, can

    def test_user_has_no_access(self):
        can = user_can_edit_dataset(self.naughty_user, self.dataset)
        assert can == False, can

    def test_user_has_no_file_access(self):
        can = user_can_edit_datafile(self.naughty_user, self.datafile)
        assert can == False, can
