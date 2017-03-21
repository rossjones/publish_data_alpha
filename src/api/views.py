import json

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from datasets.models import Location, Dataset
from datasets.logic import dataset_list, organisations_for_user


def gazeteer_lookup(request):
    q = request.GET.get('q')
    data = []
    if q:
        for l in Location.objects.filter(name__icontains=q).values():
            location_string = l['name']
            if l['location_type']:
                location_string += " ({})".format(l['location_type'])
            data.append(location_string)

    return JsonResponse(data, safe=False)


def dataset_lookup(request):
    q = request.GET.get('q')
    sort = request.GET.get('sort', 'name')
    only_user = True if request.GET.get('only_user') == '1' else False
    total, page_count, datasets = dataset_list(
        request.user, filter_query=q, sort=sort,
        only_user=only_user, fields=['title', 'name', 'published']
    )
    return JsonResponse(
        { 'total': total,
          'datasets': list(datasets)
        }, safe=False
    )


class StatusEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({})
