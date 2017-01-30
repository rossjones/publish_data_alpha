import json

from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from datasets.models import Location


def gazeteer_lookup(request):
    q = request.GET.get('q')
    data = []

    if q:
        data = ["{} ({})".format(l['name'], l['location_type'])
            for l in Location.objects.filter(name__icontains=q).values()]

    return JsonResponse(data, safe=False)


class StatusEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({})
