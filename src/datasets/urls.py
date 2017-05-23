from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import datasets.views as v


urlpatterns = [
    url(r'^new$',
        login_required(v.new_dataset),
        name='new_dataset'),

    url(r'^edit/(?P<dataset_name>[\w-]+)$',
        login_required(v.full_dataset),
        name='full_dataset'),

    # url(r'^(?P<dataset_name>[\w-]+)/organisation$',
    #     login_required(v.organisation),
    #     name='dataset_organisation'),

    url(r'^(?P<dataset_name>[\w-]+)/licence$',
        login_required(v.licence),
        name='dataset_licence'),

    url(r'^(?P<dataset_name>[\w-]+)/location$',
        login_required(v.location),
        name='dataset_location'),

    url(r'^(?P<dataset_name>[\w-]+)/frequency$',
        login_required(v.frequency),
        name='dataset_frequency'),

    # Data file URLs
    url(r'^(?P<dataset_name>[\w-]+)/addfile/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.addfile),
        name='dataset_addfile'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_weekly/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.addfile_weekly),
        name='dataset_addfile_weekly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_monthly/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.addfile_monthly),
        name='dataset_addfile_monthly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_quarterly/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.addfile_quarterly),
        name='dataset_addfile_quarterly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_annually/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.addfile_annually),
        name='dataset_addfile_annually'),

    url(r'^(?P<dataset_name>[\w-]+)/deletefile/(?P<datafile_id>[a-z\d-]+)$',
        login_required(v.deletefile),
        name='dataset_deletefile'),

    url(r'^(?P<dataset_name>[\w-]+)/confirmdeletefile/(?P<datafile_id>[a-z\d-]+)$',
        login_required(v.confirmdeletefile),
        name='dataset_confirmdeletefile'),

    url(r'^(?P<dataset_name>[\w-]+)/files$',
        login_required(v.files),
        name='dataset_files'),

    # Documentation URLs
    url(r'^(?P<dataset_name>[\w-]+)/adddoc/(?P<datafile_id>[a-z\d-]+)?$$',
        login_required(v.add_doc),
        name='dataset_adddoc'),

    url(r'^(?P<dataset_name>[\w-]+)/documents$',
        login_required(v.documents),
        name='dataset_documents'),

    url(r'^(?P<dataset_name>[\w-]+)/publish$',
        login_required(v.publish_dataset),
        name='publish_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/edit$',
        login_required(v.dataset_details),
        name='dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/confirmdelete$',
        login_required(v.confirm_delete_dataset),
        name='confirm_delete_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/delete$',
        login_required(v.delete_dataset),
        name='delete_dataset'),
]
