from django.conf.urls import url

import tasks.views as v

urlpatterns = [
    url(r'skip/(?P<task_id>\d+)$', v.skip_task, name='skip_task'),
]
