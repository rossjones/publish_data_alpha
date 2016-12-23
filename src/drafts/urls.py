from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import drafts.views as v


def get_condition_dict():
    return {
        'addfile_daily': v.show_daily_frequency,
        'addfile_never': v.show_never_frequency,
        'addfile_weekly': v.show_weekly_frequency,
        'addfile_monthly': v.show_monthly_frequency,
        'addfile_quarterly': v.show_quarterly_frequency,
        'addfile_annually': v.show_annually_frequency,
    }

dataset_wizard = login_required(
    v.DatasetWizard.as_view(
        v.FORMS,
        url_name='edit_dataset_step',
        done_step_name='done',
        condition_dict=get_condition_dict())
)

urlpatterns = [
    url(r'^new/$',
        login_required(v.DatasetCreate.as_view()),
        name='new_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/edit$',
        login_required(v.DatasetEdit.as_view()),
        name='edit_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/(?P<step>.+)$',
        dataset_wizard,
        name='edit_dataset_step'),
]
