from django.conf.urls import url

import api.views as v

urlpatterns = [
    url(r'locations$', v.gazeteer_lookup, name='gazeteer_lookup'),

    url(r'^status', v.StatusEndpoint.as_view()),
]
