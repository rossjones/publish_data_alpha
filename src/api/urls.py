from django.conf.urls import url, include

from rest_framework import routers

import api.views as v
import api.api_def as a

urlpatterns = [
    url(r'locations$', v.gazeteer_lookup, name='gazeteer_lookup'),
    url(r'^datasets$', v.dataset_lookup, name='dataset_lookup'),
    url(r'^status', v.StatusEndpoint.as_view()),

    #url(r'^1/', include(router.urls)),
    url(r'^1/datasets$', a.DatasetList.as_view()),
    url(r'^1/datasets/(?P<name>[\w-]+)$',
        a.DatasetDetail.as_view(),
        name='dataset-detail'),

    url(r'^1/organisations$', a.OrganisationList.as_view()),
    url(r'^1/organisations/(?P<name>[\w-]+)$',
        a.OrganisationDetail.as_view(),
        name='organisation-detail'),

]
