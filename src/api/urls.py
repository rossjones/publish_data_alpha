from django.conf.urls import url, include

from rest_framework import routers

import api.views as v
import api.api_def as a

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'datasets', a.DatasetViewSet)
router.register(r'organisations', a.OrganisationViewSet)

urlpatterns = [
    url(r'locations$', v.gazeteer_lookup, name='gazeteer_lookup'),
    url(r'^datasets$', v.dataset_lookup, name='dataset_lookup'),
    url(r'^status', v.StatusEndpoint.as_view()),

    url(r'^1/', include(router.urls)),
]
