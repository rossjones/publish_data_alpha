"""
Provides functions for converting between the local Draft database model
(called a Dataset) and the remote CKAN object (called a package).
"""

from datasets.models import Dataset, Datafile
from datasets.util import convert_to_slug
from .logic import dataset_show

def datafile_to_resource(datafile):
    # TODO: Add following to extras
    # start_date = models.DateField(blank=True, null=True)
    # end_date = models.DateField(blank=True, null=True)
    # month = models.IntegerField(blank=True, null=True)
    # year = models.IntegerField(blank=True, null=True)
    # quarter = models.TextField(blank=True, default="")

    return {
        'description': datafile.title,
        'url': datafile.url,
        'format': datafile.format or ''
    }


def draft_to_ckan(draft):
    return {
        "name": draft.name,
        "title": draft.title,
        "notes": draft.description,
        "owner_org": draft.organisation,
        "resources": [datafile_to_resource(r) for r in draft.files.all()],
        "license_id": draft.licence,
        "update_frequency": draft.frequency,
        "geographic_coverage": draft.countries_as_list(),
        "extras": [
            {
                "key": "notifications",
                "value": draft.notifications
            },
            {
                "key": "summary",
                "value": draft.summary
            },
            {
                "key": "licence_other",
                "value": draft.licence_other
            }
        ]
    }


def ckan_to_draft(name):
    """
    Converts a named CKAN dataset into a Dataset model
    """
    dataset = dataset_show(name)
    if not dataset:
        return None

    extras = {}
    for d in dataset['extras']:
        extras[d['key']] = d['value']

    draft = Dataset.objects.create(name=dataset['name'])
    draft.organisation = dataset['organization']['name']
    draft.frequency = dataset.get('update_frequency', 'never')
    draft.title = dataset['title']
    draft.summary = extras.get('summary', '')
    draft.description = dataset.get('notes')
    draft.licence = dataset.get('license_id')
    draft.licence_other = extras.get('licence_other', '')
    #draft.countries =
    draft.notifications = extras.get('notifications', '')
    draft.save()

    for resource in dataset.get('resources'):
        Datafile.objects.create(
            title=resource.get('description'),
            url=resource.get('url'),
            format=resource.get('format'),
            dataset=draft
        ).save()

        # TODO: Pull the following info from resource extras if
        # they are there.
        # start_date = models.DateField(blank=True, null=True)
        # end_date = models.DateField(blank=True, null=True)
        # month = models.IntegerField(blank=True, null=True)
        # year = models.IntegerField(blank=True, null=True)
        # quarter = models.TextField(blank=True, default="")

    return draft
