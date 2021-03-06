import uuid

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from tasks.models import Task
from tasks.logic import get_tasks_for_user, get_tasks_for_organisation

from datasets.logic import organisations_for_user
from datasets.models import Organisation, Dataset


class TasksTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username="Test User",
            email="test-signin@localhost",
            apikey=str(uuid.uuid4())
        )
        self.test_user.set_password("password")
        self.test_user.save()

        self.organisation = Organisation.objects.create(
            name='test-org',
            title='Test Organisation',
            description='Test Organisation Description'
        )
        self.organisation.users.add(self.test_user)

        self.org_names = [self.organisation.name]

        self.dataset = Dataset.objects.create(name='test', title='Test',
                                              creator=self.test_user)

        self.simple_task_update = Task.objects.create(
            owning_organisation=self.org_names[0],
            required_permission_name="",
            description="Task description",
            category="update",
            related_object_id='test'
        )
        self.simple_task_fix = Task.objects.create(
            owning_organisation=self.org_names[0],
            required_permission_name="",
            description="Task description",
            category="fix",
            related_object_id='test'
        )

    def test_ok(self):
        tasks = get_tasks_for_user(self.test_user)
        assert len(tasks['update']) == 1

    def test_my_tasks(self):
        response = self.client.post(reverse('signin'), {
            "email": "test-signin@localhost",
            "password": "password"
        })
        assert response.status_code == 302

        tasks = get_tasks_for_organisation('test-org')
        assert len(tasks['update']) == 1

        tasks = get_tasks_for_user(self.test_user)
        assert len(tasks['update']) == 1
