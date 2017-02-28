from django.conf.urls import url

import tasks.views as v

urlpatterns = [
    url(r'organisation$', v.organisation_tasks, name='organisation_tasks'),
    url(r'skip/(?P<task_id>\d+)$', v.skip_task, name='skip_task'),
    url(r'$', v.my_tasks, name='my_tasks'),
]
