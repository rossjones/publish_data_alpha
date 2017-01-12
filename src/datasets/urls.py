from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import datasets.views as v


urlpatterns = [
    url(r'^new$',
        login_required(v.new_dataset),
        name='new_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/organisation$',
        login_required(v.edit_organisation),
        name='edit_dataset_organisation'),

    url(r'^(?P<dataset_name>[\w-]+)/licence$',
        login_required(v.edit_licence),
        name='edit_dataset_licence'),

    url(r'^(?P<dataset_name>[\w-]+)/location$',
        login_required(v.edit_location),
        name='edit_dataset_location'),

    url(r'^(?P<dataset_name>[\w-]+)/frequency$',
        login_required(v.edit_frequency),
        name='edit_dataset_frequency'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile$',
        login_required(v.edit_addfile),
        name='edit_dataset_addfile'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_weekly$',
        login_required(v.edit_addfile_weekly),
        name='edit_dataset_addfile_weekly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_monthly$',
        login_required(v.edit_addfile_monthly),
        name='edit_dataset_addfile_monthly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_quarterly$',
        login_required(v.edit_addfile_quarterly),
        name='edit_dataset_addfile_quarterly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_annually$',
        login_required(v.edit_addfile_annually),
        name='edit_dataset_addfile_annually'),

    url(r'^(?P<dataset_name>[\w-]+)/files$',
        login_required(v.edit_files),
        name='edit_dataset_files'),

    url(r'^(?P<dataset_name>[\w-]+)/notifications$',
        login_required(v.edit_notifications),
        name='edit_dataset_notifications'),


    url(r'^(?P<dataset_name>[\w-]+)/check_dataset$',
        login_required(v.check_dataset),
        name='edit_dataset_check_dataset'),


    url(r'^(?P<dataset_name>[\w-]+)/edit$',
        login_required(v.edit_dataset_details),
        name='edit_dataset'),


    url(r'^(?P<dataset_name>[\w-]+)/delete$',
        login_required(v.delete_dataset),
        name='delete_dataset'),
]
