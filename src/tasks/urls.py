from django.conf.urls import url

import tasks.views as v

urlpatterns = [
    url(r'organisation$', v.organisation_tasks, name='organisation_tasks'),
    url(r'$', v.my_tasks, name='my_tasks'),
]
