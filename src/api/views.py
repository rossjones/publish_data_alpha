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
        for l in Location.objects.filter(name__icontains=q).values():
            location_string = l['name']
            if l['location_type']:
                location_string += " ({})".format(l['location_type'])
            data.append(location_string)

    return JsonResponse(data, safe=False)


class StatusEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({})
