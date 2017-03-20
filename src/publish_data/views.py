import os
import json

from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import ugettext as _

from datasets.logic import dataset_list, organisations_for_user
from tasks.logic import get_tasks_for_user
from stats.logic import get_stats
from runtime_config.logic import get_config


def _query_string(q, sort):
    qsp = {}
    if sort:
        qsp['sort'] = sort
    if q:
        qsp['q'] = q
    qs = urlencode(qsp)
    if qs != '':
        qs = '?' + qs
    return qs


def _manage_context(request, only_user, view_name):
    q = request.GET.get('q')
    sort = request.GET.get('sort')

    page = 1
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    if sort == 'name':
        sort_name_next = '-name'
        sort_published_next = 'published'
    elif sort == '-name':
        sort_name_next = ''
        sort_published_next = 'published'
    elif sort == 'published':
        sort_name_next = 'name'
        sort_published_next = '-published'
    elif sort == '-published':
        sort_name_next = 'name'
        sort_published_next = ''
    else:
        sort_name_next = 'name'
        sort_published_next = 'published'

    if sort and not sort in ['name', 'published', '-name', '-published']:
        sort = None

    total, page_count, datasets = dataset_list(
        request.user, page, filter_query=q, sort=sort, only_user=only_user
    )

    ckan_host = get_config('ckan.host') or ''

    organisation = request.user.primary_organisation()

    return {
        "current_view": view_name,
        "datasets": datasets,
        "organisation": organisation,
        "total": total,
        "page_range": range(1, page_count),
        "current_page": page,
        "q": q or "",
        "find_url": settings.FIND_URL or ckan_host,
        "sort": sort,
        "qs_name_next": reverse(view_name) + \
            _query_string(q, sort_name_next),
        "qs_published_next": reverse(view_name) + \
            _query_string(q, sort_published_next)
    }

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('my_tasks'))

    return render(request, "home.html", {})


@login_required()
def manage_my_data(request):
    context = _manage_context(request, True, 'manage_my_data')
    return render(request, "manage/my.html", context)


@login_required()
def manage_org_data(request):
    context = _manage_context(request, False, 'manage_org_data')
    return render(request, "manage/organisation.html", context)
