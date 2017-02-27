import uuid
import json

from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings
from django.utils.translation import ugettext as _
from autoslug import AutoSlugField

from datasets.util import (calculate_dates_for_month,
                           calculate_dates_for_quarter,
                           calculate_dates_for_year)



class Location(models.Model):

    name = models.CharField(max_length=256)
    location_type = models.CharField(max_length=64, null=True)


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = AutoSlugField(populate_from='title', default='', unique=True, max_length=200)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200, default="")
    description = models.TextField()

    # register, its, inspire etc.
    dataset_type = models.CharField(max_length=200, default="")

    # References the organisation by its short name
    organisation = models.ForeignKey(
        'Organisation',
        related_name='datasets',
        null=True
    )

    # ogl, other
    licence = models.CharField(max_length=64, default="", blank=True)
    licence_other = models.TextField(default="", blank=True)

    location1 = models.TextField(default="", blank=True)
    location2 = models.TextField(default="", blank=True)
    location3 = models.TextField(default="", blank=True)

    frequency = models.TextField(default="", blank=True, null=True)

    notifications = models.TextField(default="", blank=True)

    last_edit_date = models.DateTimeField(auto_now=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True)

    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True, blank=True)

    is_harvested = models.BooleanField(default=False)
    legacy_metadata = models.TextField(null=True, blank=True)


    def noun(self):
        if self.published:
            return _('Dataset')
        return _('Draft')


    def status_text(self):
        if self.published:
            return _('Published')
        return _('Draft')


    def as_dict(self):
        def _strip_location(loc):
            if not loc or not loc.strip():
                return ''

            idx = loc.find('(')
            if idx < 0:
                idx = len(loc)
            return loc[0:idx].strip()

        data = {
            'id': str(self.id),
            'name': self.name,
            'title': self.title,
            'summary': self.summary,
            'notes': self.description,
            'dataset_type': self.dataset_type,
            'licence': self.licence,
            'licence_other': self.licence_other or '',
            'location1': _strip_location(self.location1),
            'location2': _strip_location(self.location2),
            'location3': _strip_location(self.location3),
            'update_frequency': self.frequency,
            'last_edit_date': self.last_edit_date.isoformat(),
            'published_date': self.published_date.isoformat() if self.published_date else '',
            'organisation_name': self.organisation.name,
            'organisation': self.organisation.as_dict(),
            'resources': [f.as_dict() for f in self.files.filter(is_documentation=False).all()],
            'documentation': [f.as_dict() for f in self.files.filter(is_documentation=True).all()],
            'inspire': {}
        }

        if self.dataset_type == 'inspire':
            inspire = getattr(self, 'inspire')
            data['inspire'] = inspire.as_dict()


        return data

    def __str__(self):
        return u"{}:{}".format(self.name, self.title)

class InspireDataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    bbox_east_long = models.CharField(max_length=64, null=True, blank=True)
    bbox_west_long = models.CharField(max_length=64, null=True, blank=True)
    bbox_north_lat = models.CharField(max_length=64, null=True, blank=True)
    bbox_south_lat = models.CharField(max_length=64, null=True, blank=True)

    coupled_resource = models.TextField(null=True, blank=True)
    dataset_reference_date = models.TextField(null=True, blank=True)
    frequency_of_update = models.CharField(max_length=64, null=True, blank=True)
    guid = models.CharField(max_length=128, blank=True, null=True)
    harvest_object_id = models.TextField(null=True, blank=True)
    harvest_source_reference = models.TextField(null=True, blank=True)
    import_source = models.TextField(null=True, blank=True)
    metadata_date = models.CharField(max_length=64, null=True, blank=True)
    metadata_language = models.CharField(max_length=64, null=True, blank=True)
    provider = models.TextField(null=True, blank=True)
    resource_type = models.CharField(max_length=64, null=True, blank=True)
    responsible_party = models.TextField(null=True, blank=True)

    spatial = models.TextField(null=True, blank=True)
    spatial_data_service_type = models.CharField(max_length=64, null=True, blank=True)
    spatial_reference_system = models.CharField(max_length=128, null=True, blank=True)

    dataset = models.OneToOneField(Dataset, related_name='inspire')

    def as_dict(self):
        return model_to_dict(self)


class Datafile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=64)
    url = models.URLField(max_length=2048)
    format = models.CharField(max_length=32, blank=True)
    dataset = models.ForeignKey(Dataset, related_name="files")
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    quarter = models.IntegerField(blank=True, null=True)

    is_broken = models.BooleanField(default=False)
    last_check = models.DateTimeField(null=True, blank=True)

    is_documentation = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not (self.start_date and self.end_date):
            if self.quarter and self.year:
                self.start_date, self.end_date = \
                    calculate_dates_for_quarter(self.quarter, self.year)
            elif self.year and self.month:
                self.start_date, self.end_date = \
                    calculate_dates_for_month(self.month, self.year)
            elif self.year:
                self.start_date, self.end_date = \
                    calculate_dates_for_year(self.year)

        super(Datafile, self).save(*args, **kwargs)

    def as_dict(self):
        start, end = self.start_date, self.end_date
        data = {
            'id': str(self.id),
            'title': self.title,
            'url': self.url,
            'format': self.format,
            'start_date': start.isoformat() if start else None,
            'end_date': end.isoformat() if end else None,
            'is_broken': self.is_broken
        }

        return data

    def __str__(self):
        return u"{}/{}".format(self.title, self.url)


class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200, default="", blank=True)
    title = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField()
    abbreviation = models.CharField(max_length=200, default="", null=True, blank=True)

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

    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='organisations')

    def as_dict(self):
        data = {
            'id': str(self.id),
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'abbreviation': self.abbreviation or '',
            'contact_email': self.contact_email or '',
            'contact_name': self.contact_name or '',
            'contact_phone': self.contact_phone or '',
            'foi_email': self.foi_email or '',
            'foi_name': self.foi_name or '',
            'foi_phone': self.foi_phone or '',
            'foi_web': self.foi_web or '',
            'closed': self.closed,
            'replaced_by': self.replaced_by,
        }

        return data

    def __str__(self):
        return self.title
