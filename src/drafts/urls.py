from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import drafts.views as v


dataset_wizard = login_required(
    v.DatasetWizard.as_view(
        v.FORMS,
        url_name='edit_dataset_step',
        done_step_name='done',
        condition_dict={
            'frequency_weekly': v.show_weekly_frequency,
            'frequency_monthly': v.show_monthly_frequency,
            'frequency_quarterly': v.show_quarterly_frequency,
            'frequency_annually': v.show_annually_frequency,
        })
)

urlpatterns = [
    url(r'^new/$',
        login_required(v.DatasetCreate.as_view()),
        name='new_dataset'),

    url(r'edit/^(?P<dataset_name>[\w-]+)$',
        login_required(v.DatasetEdit.as_view()),
        name='edit_dataset_full'),

    url(r'^(?P<dataset_name>[\w-]+)/(?P<step>.+)$',
        dataset_wizard,
        name='edit_dataset_step'),
]
