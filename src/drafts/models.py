import ast

from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings

class Dataset(models.Model):
    name = models.CharField(max_length=64, default="")
    title = models.CharField(max_length=64)
    description = models.TextField()

    # ogl, inspire, other
    licence = models.CharField(max_length=64, default="")
    licence_other = models.TextField(default="", blank=True)

    countries = models.TextField(default="[]")
    frequency = models.TextField(default="", blank=True)
    notifications = models.TextField(default="", blank=True)

    last_edit_date = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def as_dict(self):
        current = model_to_dict(self)
        current['themes'] = ast.literal_eval(current.get('themes', '[]'))
        current['countries'] = ast.literal_eval(current.get('countries', '[]'))
        return current


class Datafile(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField()
    dataset = models.ForeignKey(Dataset, related_name="files")
