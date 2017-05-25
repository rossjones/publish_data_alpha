from django.db.models import Q
from tasks.models import Task, TASK_CATEGORIES
from datasets.models import Dataset
from datasets.logic import organisations_for_user


def get_tasks_for_user(user):
    """ For the given user, find the tasks that
        they have in each category based on:
            * Their organisation membership
            * Them having the required permissions
            * Them not having skipped it before.
    """
    orgs = [o.name for o in organisations_for_user(user)]
    user_permissions = [""]

    user_datasets = Dataset.objects.filter(
        owner=user).values_list(
        'name', flat=True)

    task_objs = Task.objects\
        .filter(owning_organisation__in=orgs)\
        .filter(required_permission_name__in=user_permissions)\
        .filter(related_object_id__in=user_datasets)\
        .all()

    tasks = {}
    for entry in TASK_CATEGORIES:
        tasks[entry[0]] = [t for t in task_objs if t.category == entry[0]]

    return tasks


def get_tasks_for_organisation(organisation):
    """ For the given organisation name, find the tasks that
        they have in each category
    """
    orgs = [organisation]
    user_permissions = [""]
    task_objs = Task.objects\
        .filter(owning_organisation__in=orgs)\
        .filter(required_permission_name__in=user_permissions)\
        .all()

    tasks = {}
    for entry in TASK_CATEGORIES:
        tasks[entry[0]] = [t for t in task_objs if t.category == entry[0]]

    return tasks
