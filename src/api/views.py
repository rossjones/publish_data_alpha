import json

from django.http import HttpResponse
from django.shortcuts import render

from api.models import Location


def gazeteer_lookup(request):
    q = request.GET.get('q')
    data = []

    if q:
        data = Location.objects.filter(name__istartswith=q).all()
        data = [n.name for n in data]

    return HttpResponse(json.dumps(data), content_type='application/json')
