import math

from datasets.models import Dataset, Organisation


def organisations_for_user(user):
    return user.organisation_set.all()


def dataset_list(user, page=1, filter_query=None):
    """
    For the given user returns a tuple containing total number of datasets
    both draft and published, and the 20 most recent.

    TODO: Get this from a search index.
    """
    per_page = 20
    max_fetch = per_page * page

    organisations = organisations_for_user(user)
    q = Dataset.objects\
        .filter(organisation__in=organisations)

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

def get_a_ckan():
    return None

def make_alpha_id(dataset):
    '''
    Use properties of the dataset to generate an alpha id. This isn't
    intended to be secure, it's just intended to not be obviously an ID.
    '''
    return hashlib.md5(bytes(dataset.id)).hexdigest()

def convert_to_ckan(dataset):
    '''
    Convert from our local database structure into a format that
    we can push to a CKAN.
    '''
    return {}


def find_ckan_dataset(ckan, name):
    '''
    Find any existing dataset with the same name as our local dataset
    where the alpha_id is not present in the extras. If we find it, we
    will package_update.  If we do not find it we will publish. If
    we find a dataset without the alpha_id we will increment the number
    in the name and go around the loop again.
    '''
    return '', False


def publish_to_ckan(dataset):
    # The dataset MUST have been published.
    if not dataset.published:
        return None

    # The configuration for where to publish must be available and active
    ckan = get_a_ckan()
    if not ckan:
        return None

    # Find the name under which we want to publish this dataset, and
    # if necessary set the local name to match. Also tells us whether
    # to update or create.
    name, update = find_ckan_dataset(ckan, dataset.name)
    if name != dataset.name:
        dataset.name = name
        dataset.save()

    # Prepare the dataset for publishing in CKAN format.


    # Publish the dataset to CKAN
    if update:
        # package_update
        pass
    else:
        # package_create
        pass










