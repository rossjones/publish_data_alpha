import ast

from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings

class Location(models.Model):

    name = models.CharField(max_length=256)
    location_type = models.CharField(max_length=64, null=True)


class Dataset(models.Model):
    name = models.CharField(max_length=64, default="")
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=200, default="")
    description = models.TextField()

    # References the organisation by its short name
    organisation = models.CharField(max_length=128, default="")

    # ogl, inspire, other
    licence = models.CharField(max_length=64, default="")
    licence_other = models.TextField(default="", blank=True)

    location = models.TextField(default="")
    frequency = models.TextField(default="", blank=True)

    notifications = models.TextField(default="", blank=True)

    last_edit_date = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True)

    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)

    legacy_metadata = models.TextField(null=True)

    def as_dict(self):
        current = model_to_dict(self)
        return current

    def __str__(self):
        return u"{}:{}".format(self.name, self.title)


class Datafile(models.Model):
    title = models.CharField(max_length=128)
    url = models.URLField()
    format = models.CharField(max_length=16, blank=True)
    dataset = models.ForeignKey(Dataset, related_name="files")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    quarter = models.TextField(blank=True, default="")

    def __str__(self):
        return u"{}/{}".format(self.title, self.url)
