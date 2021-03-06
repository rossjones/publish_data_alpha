import math
from datetime import datetime, timedelta

from django.db.models import Q
from datasets.models import Dataset, Organisation
from datasets.search import index_dataset
from datasets.search import delete_dataset as unindex_dataset


def organisations_for_user(user):
    if user.is_staff:
        return Organisation.objects.all()
    return user.organisations.all()


def publish(dataset, user):
    if dataset.published:
        publish_to_ckan(dataset, user)
        index_dataset(dataset)
    else:
        unindex_dataset(dataset)


def dataset_list(
        user,
        page=1,
        filter_query=None,
        sort=None,
        only_user=False,
        fields=None):
    """
    For the given user returns a tuple containing total number of datasets
    both draft and published, and the 20 most recent.
    """
    per_page = 20
    max_fetch = per_page * page

    organisations = organisations_for_user(user)

    sub_query = Q(organisation__in=organisations) & Q(owner=user) \
        if only_user else Q(organisation__in=organisations)

    q = Dataset.objects.filter(sub_query)

    if filter_query:
        q = q.filter(title__icontains=filter_query)

    if not sort:
        q = q.order_by('-last_edit_date')
    else:
        q = q.order_by(sort)

    start = (per_page * page) - per_page
    if fields:
        q = q.values(*fields)

    datasets = q.all()[start:start + per_page]

    total = q.count()
    page_count = math.ceil(float(total) / per_page)

    offset = (page * per_page) - per_page
    return (total, page_count, datasets,)


def is_dataset_overdue(dataset):
    recent_date = most_recent_datafile(dataset)
    if not recent_date:
        return False

    num_days = number_days_for_frequency(dataset.frequency)
    diff = recent_date + timedelta(days=num_days)
    return datetime.now().date() > diff


def most_recent_datafile(dataset):
    ''' Iterates through the files in the dataset, and find the
    one with the most recent start-date, returning the start date '''
    dates = [f.start_date for f in dataset.files.all() if f.start_date]
    dates.sort(reverse=True)
    return dates[0] if dates else None


def number_days_for_frequency(frequency):
    if frequency == 'annually':
        return 365
    elif frequency == 'monthly':
        return 30
    elif frequency == 'weekly':
        return 7
    elif frequency == 'quarterly':
        return 90
    return 0

###########################################################################
# The functions below are intended only for use in Alpha, until a working
# find_data is available.  They will push published datasets to a CKAN
# instance should the configuration be available to do so.
#
# We will identify alpha-published datasets from an extra added to each
# dataset published, and we will use this when looking for existing dataset
# names when we publish from here (updating the local Dataset to use the
# name that it was actually published under).  Any changes on the CKAN
# instance WILL NOT be reflected in the Alpha publish_data.
###########################################################################


import hashlib
import json
import requests


def get_ckan(user):
    """ Returns a CKAN instance if configuration contains both a host
    and a key.  If not, returns None
    """
    from runtime_config.logic import get_config
    from ckanapi import RemoteCKAN

    ckan_host = get_config('ckan.host')
    if not (ckan_host and user.apikey):
        return None

    return RemoteCKAN(ckan_host, apikey=user.apikey)


def make_alpha_id(dataset):
    """ Use id of the dataset to generate an alpha id. This isn't
    intended to be secure, it's just intended to not be obviously an ID.
    """
    return hashlib.md5(dataset.id.bytes).hexdigest()


def convert_to_ckan(dataset, alpha_id):
    """ Convert from our local database structure into a format that
    we can push to a CKAN instance.
    """
    data = {
        'name': dataset.name,
        'title': dataset.title,
        'notes': '{}\n\n{}'.format(dataset.summary, dataset.description),
        'owner_org': dataset.organisation.name,
        'license_id': dataset.licence,
        'extras': [
            {'key': 'alpha_id', 'value': alpha_id},
            {'key': 'update_frequency', 'value': dataset.frequency or ''},
            {'key': 'location', 'value': dataset.location or ''},
        ],
        'resources': []
    }

    if dataset.licence == 'other':
        data['extras'].append({
            'key': 'licence_other', 'value': dataset.licence_other
        })

    for file in dataset.files.all():
        r = {
            'description': file.name,
            'url': file.url,
            'format': file.format or '',
            'is_broken': file.is_broken,
        }
        if file.is_documentation:
            r['resource_type'] = 'documentation'
        data['resources'].append(r)

    return data


def get_alpha_id(ckan_dataset):
    for extra in ckan_dataset.get('extras', []):
        if extra.get('key') == 'alpha_id':
            return extra.get('value')
    return None


def find_ckan_dataset(ckan, current_name, alpha_id):
    """ Looks for the first name we can use for this dataset.
    We may find an existing dataset with this name, and no
    alpha id, in which case we will try a different name.  We
    may find an existing with an alpha_id, in which case we
    will use this one. We may find nothing, in which case
    we're good to go.
    """
    from ckanapi.errors import NotFound
    name = current_name

    while True:
        try:
            res = ckan.action.package_show(id=name)
        except NotFound:
            # Does not currently exist, not an update.
            return name, False

        if get_alpha_id(res) == alpha_id:
            return name, True

        # name is in use, modify it and try again.
        name = name + "-1"

    return None, False


def publish_to_ckan(dataset, user):
    # The dataset MUST have been published.
    if not dataset.published:
        return "Dataset is not published"

    if not user.apikey:
        return "User has no API key"

    # The configuration for where to publish must be available and active
    ckan = get_ckan(user)
    if not ckan:
        return "CKAN is not configured"

    alpha_id = make_alpha_id(dataset)

    # Find the name under which we want to publish this dataset, and
    # if necessary set the local name to match. Also tells us whether
    # to update or create.
    name, update = find_ckan_dataset(ckan, dataset.name, alpha_id)
    if name != dataset.name:
        dataset.name = name
        dataset.save()

    # Prepare the dataset for publishing in CKAN format.
    data = convert_to_ckan(dataset, alpha_id)

    # Publish the dataset to CKAN
    f = ckan.action.package_create
    if update:
        f = ckan.action.package_update

    try:
        f(**data)
    except Exception as e:
        return str(e)

    return ""
