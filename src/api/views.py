import json

from django.http import HttpResponse
from django.shortcuts import render

from datasets.models import Location


def gazeteer_lookup(request):
    q = request.GET.get('q')
    data = []

    if q:
        data = [l for l in
            Location.objects.filter(name__istartswith=q).values()]

    return HttpResponse(json.dumps(data), content_type='application/json')
