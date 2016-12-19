from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from ckan_proxy.logic import organization_list_for_user
from ckan_proxy.util import test_user_key

from tasks.models import Task
from tasks.logic import get_tasks_for_user, user_ignore_task


class TasksTestCase(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            username="Test User",
            email="test-signin@localhost",
            apikey=test_user_key()
        )
        self.test_user.set_password("password")
        self.test_user.save()

        self.org_names = [o['name'] for o in
                          organization_list_for_user(self.test_user)]

        self.simple_task_update = Task.objects.create(
            owning_organisation=self.org_names[0],
            required_permission_name="",
            description="Task description",
            category="update"
        )
        self.simple_task_fix = Task.objects.create(
            owning_organisation=self.org_names[0],
            required_permission_name="",
            description="Task description",
            category="fix"
        )
        self.simple_task_improve = Task.objects.create(
            owning_organisation=self.org_names[0],
            required_permission_name="",
            description="Task description",
            category="improve"
        )

    def test_ok(self):
        tasks = get_tasks_for_user(self.test_user)
        assert len(tasks['update']) == 1

    def test_hide(self):
        tasks = get_tasks_for_user(self.test_user)
        assert len(tasks['fix']) == 1

        user_ignore_task(self.test_user, self.simple_task_fix)

        tasks = get_tasks_for_user(self.test_user)
        assert len(tasks['fix']) == 0, tasks['fix']

    def test_hide_web(self):
        response = self.client.post(reverse('signin'), {
            "email": "test-signin@localhost",
            "password": "password"
        })
        assert response.status_code == 302

        tasks = get_tasks_for_user(self.test_user)
        assert len(tasks['improve']) == 1

        resp = self.client.get(reverse('skip_task',
                               args=[tasks['improve'][0].id]))
        assert resp.status_code == 302
        assert resp.url == "/", resp.url
