from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from datasets.models import Dataset
from tasks.models import Task
from tasks.logic import get_tasks_for_user, get_tasks_for_organisation


@login_required()
def my_tasks(request):
    organisation = request.user.primary_organisation()
    datasets = Dataset.objects.all()
    tasks = get_tasks_for_user(request.user)

    return render(request, "tasks/my.html", {
        'organisation': organisation,
        'tasks': tasks,
        'datasetsUpdate': datasets[13443:13500],
        'datasetsBroken': datasets[22342:22400],
    })


@login_required()
def organisation_tasks(request):
    organisation = request.user.primary_organisation()
    datasets = Dataset.objects.all()
    tasks = get_tasks_for_organisation(organisation.name)

    return render(request, "tasks/organisation.html", {
        'organisation': organisation,
        'tasks': tasks,
        'datasetsUpdate': datasets[11020:11055],
        'datasetsBroken': datasets[22342:22400],
    })
