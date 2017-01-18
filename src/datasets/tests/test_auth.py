import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datasets.models import Dataset, Organisation, Datafile
from datasets.auth import user_can_edit_dataset, user_can_edit_datafile


class AuthTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email="test-signin@localhost",
            username="Test User Signin",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

        self.naughty_user = get_user_model().objects.create(
            email="naughty-user@localhost",
            username="Naughty Test User Signin",
            apikey=str(uuid.uuid4())
        )

        self.organisation = Organisation.objects.create(
            name='test-org',
            title='Test Organisation',
            description='Test Organisation Description'
        )
        self.organisation.users.add(self.test_user)

        # Log the user in
        self.client.post(reverse('signin'), {
            "email": "test-signin@localhost",
            "password": "password"
        })

        # Both test the initial dataset creation, and get a name we can
        # use for the remaining tests.
        self.dataset_name = self._create_new_dataset()
        self.dataset = Dataset.objects.get(name=self.dataset_name)
        self.dataset.organisation = self.organisation
        self.dataset.save()

        self.datafile = Datafile.objects.create(
            title="A test file",
            url="https://data.gov.uk",
            format="HTML",
            dataset=self.dataset)



    def _create_new_dataset(self):
        response = self.client.post(reverse('new_dataset', args=[]), {
                'title': 'A test dataset for create',
                'description': 'A test description',
                'summary': 'A test summary',
        })
        assert response.status_code == 302

        parts = response.url.split('/')
        name = parts[2]

        # Set frequency
        response = self.client.post(reverse('edit_dataset_frequency', args=[name]), {
                'frequency': 'weekly',
        })
        assert response.status_code == 302

        return name

    def test_user_has_access(self):
        can = user_can_edit_dataset(self.test_user, self.dataset)
        assert can == True, can

    def test_user_has_file_access(self):
        can = user_can_edit_datafile(self.test_user, self.datafile)
        assert can == True, can

    def test_user_has_no_access(self):
        can = user_can_edit_dataset(self.naughty_user, self.dataset)
        assert can == False, can

    def test_user_has_no_file_access(self):
        can = user_can_edit_datafile(self.naughty_user, self.datafile)
        assert can == False, can



