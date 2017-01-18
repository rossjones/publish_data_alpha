"""
Because some views are dependent on the presence of values from previous form
submissions, we need to fake the function called at runtime to say we always
want the addfile_weekly form to be showed
"""
def _show_weekly_for_test(x):
    return True

import datasets.views as v
v.show_weekly_frequency = _show_weekly_for_test


