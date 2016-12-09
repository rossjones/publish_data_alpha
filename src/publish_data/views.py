import math

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from publish_data.logic import dataset_list

def home(request):
    if request.user.is_authenticated():
        return dashboard(request)
    return render(request, "home.html", {})

def dashboard(request):
    return render(request, "dashboard.html", {})

@login_required()
def manage_data(request):
    # TODO: Determine default sort order, most recent first with drafts
    # and published interspersed? Paging the remote datasets will be a
    # pain
    page = 1
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    total, page_count, datasets = dataset_list(request.user, page)

    return render(request, "manage.html", {
        "datasets": datasets,
        "total": total,
        "page_range": range(1, page_count),
        "current_page": page
    })
