from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from datasets.logic import dataset_list
from tasks.logic import get_tasks_for_user
from stats.logic import get_stats

def home(request):
    if request.user.is_authenticated():
        return dashboard(request)
    return render(request, "home.html", {})


@login_required()
def dashboard(request):
    tasks = get_tasks_for_user(request.user)
    # Use an actual organisation for this user
    stats = get_stats("cabinet-office", "Downloads")

    return render(request, "dashboard.html", {
        "tasks": tasks,
        "stats": stats
    })


@login_required()
def manage_data(request):

    q = request.GET.get('q')
    new_set = request.GET.get('newset')
    deleted = request.GET.get('deleted')

    page = 1
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    total, page_count, datasets = dataset_list(
        request.user, page, filter_query=q
    )

    return render(request, "manage.html", {
        "datasets": datasets,
        "total": total,
        "page_range": range(1, page_count),
        "current_page": page,
        "q": q or "",
        "newset": new_set or "",
        "deleted": deleted or ""
    })
