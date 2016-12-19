from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from tasks.models import Task
from tasks.logic import user_ignore_task


@login_required()
def skip_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    user_ignore_task(request.user, task)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
