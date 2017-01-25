import math

from datasets.models import Dataset, Organisation


def organisations_for_user(user):
    if user.is_staff:
        return Organisation.objects.all()
    return user.organisations.all()


def dataset_list(user, page=1, filter_query=None):
    """
    For the given user returns a tuple containing total number of datasets
    both draft and published, and the 20 most recent.

    TODO: Get this from a search index.
    """
    per_page = 20
    max_fetch = per_page * page

    q = Dataset.objects\
        .filter(creator=user)

    if filter_query:
        q = q.filter(title__icontains=filter_query)

    q = q.order_by('-last_edit_date')

    datasets = q.all()[0:max_fetch]


    #results = datasets_for_user(
    #    user,
    #    search_term=filter_query or "*:*",
    #)


    total = q.count()
    page_count = math.ceil(float(total) / per_page)

    offset = (page * per_page) - per_page
    return (total, page_count, datasets,)


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

def get_ckan():
    """ Returns a CKAN instance if configuration contains both a host
    and a key.  If not, returns None
    """
    from runtime_config.logic import get_config
    from ckanapi import RemoteCKAN

    ckan_host = get_config('ckan.host')
    ckan_key =  get_config('ckan.apikey')
    if not (ckan_host and ckan_key):
        return None

    return RemoteCKAN(ckan_host, apikey=ckan_key)


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
            {'key': 'location', 'value': dataset.location or ''} ,
        ],
        'resources': []
    }

    if dataset.licence == 'other':
        data['extras'].append({
            'key': 'licence_other', 'value': dataset.licence_other
        })

    for file in dataset.files.all():
        r = {
            'description': file.title,
            'url': file.url,
            'format': file.format or '',
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


def publish_to_ckan(dataset):
    # The dataset MUST have been published.
    if not dataset.published:
        return "Dataset is not published"

    # The configuration for where to publish must be available and active
    ckan = get_ckan()
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
