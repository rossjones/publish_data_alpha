import ast
import uuid

from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings

from autoslug import AutoSlugField


class Location(models.Model):

    name = models.CharField(max_length=256)
    location_type = models.CharField(max_length=64, null=True)


class Dataset(models.Model):
    #name = models.CharField(max_length=64, default="")
    name = AutoSlugField(populate_from='title', default='', unique=True)
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=200, default="")
    description = models.TextField()

    # References the organisation by its short name
    organisation = models.ForeignKey(
        'Organisation',
        related_name='datasets',
        null=True
    )

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
    published_date = models.DateTimeField(null=True, blank=True)

    legacy_metadata = models.TextField(null=True, blank=True)

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


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200, default="", blank=True)
    title = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField()
    abbreviation = models.CharField(max_length=32, default="", null=True, blank=True)

    created = models.DateTimeField(auto_now=True)

    closed = models.BooleanField(default=False)
    replaced_by = models.CharField(max_length=200, default="", blank=True)

    contact_email = models.CharField(max_length=200, default="", blank=True)
    contact_name = models.CharField(max_length=200, default="", blank=True)
    contact_phone = models.CharField(max_length=200, default="", blank=True)
    foi_email = models.CharField(max_length=200, default="", blank=True)
    foi_name = models.CharField(max_length=200, default="", blank=True)
    foi_phone = models.CharField(max_length=200, default="", blank=True)
    foi_web = models.CharField(max_length=200, default="", blank=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title
