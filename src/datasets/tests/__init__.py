from django.conf import settings
settings.ES_INDEX = 'data_discovery_test'

# Reset any existing test index before use
from datasets.search import reset_index
reset_index()

"""
Because some views are dependent on the presence of values from previous form
submissions, we need to fake the function called at runtime to say we always
want the addfile_weekly form to be showed
"""
def _show_weekly_for_test(x):
    return True

import datasets.views as v
v.show_weekly_frequency = _show_weekly_for_test


def setup():
    print("Setting up test data for 'datasets'")
