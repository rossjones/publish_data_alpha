import math
import pytz

from dateutil.parser import parse as parse_date
from django.utils.translation import ugettext as _

from datasets.models import Dataset
from datasets.logic import organisations_for_user

utc = pytz.UTC


def dataset_list(user, page=1, filter_query=None):
    """
    For the given user returns a tuple containing total number of datasets
    both draft and published, and the 20 most recent.

    TODO: Get this from a search index.
    """
    per_page = 20
    max_fetch = per_page * page

    # Find relevant datasets from CKAN
    organisations = organisations_for_user(user)
    q = Dataset.objects\
        .filter(organisation__in=organisations)\
        .order_by('last_edit_date')

    datasets = q.all()[0:max_fetch]


    #results = datasets_for_user(
    #    user,
    #    search_term=filter_query or "*:*",
    #)


    total = q.count()
    page_count = math.ceil(float(total) / per_page)

    offset = (page * per_page) - per_page
    return (total, page_count, datasets,)
