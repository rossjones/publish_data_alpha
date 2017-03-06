from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from tasks.models import Task
from tasks.logic import get_tasks_for_user, get_tasks_for_organisation


@login_required()
def my_tasks(request):
    organisation = request.user.primary_organisation()

    tasks = get_tasks_for_user(request.user)

    return render(request, "tasks/my.html", {
        'organisation': organisation,
        'tasks': tasks,
    })

@login_required()
def organisation_tasks(request):
    organisation = request.user.primary_organisation()
    tasks = get_tasks_for_organisation(organisation.name)

    return render(request, "tasks/organisation.html", {
        'organisation': organisation,
        'tasks': tasks,
    })
