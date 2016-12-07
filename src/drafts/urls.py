from django.conf.urls import url

import drafts.views as v

urlpatterns = [
    url(r'new$', v.DatasetCreate.as_view(), name='new_dataset'),
    url(r'edit/(?P<dataset_name>[\w-]+)$',
        v.DatasetFullEditView.as_view(),
        name='edit_dataset_full'),

    url(r'(?P<dataset_name>[\w-]+)/edit$',
        v.DatasetEditView.as_view(),
        name='edit_dataset'),
    url(r'(?P<dataset_name>[\w-]+)/country$',
        v.EditCountryView.as_view(),
        name='edit_country'),
    url(r'(?P<dataset_name>[\w-]+)/licence$',
        v.EditLicenceView.as_view(),
        name='edit_licence'),
    url(r'(?P<dataset_name>[\w-]+)/frequency$',
        v.EditFrequencyView.as_view(),
        name='edit_frequency'),
    url(r'(?P<dataset_name>[\w-]+)/add$',
        v.AddFileView.as_view(),
        name='edit_addfile'),
    url(r'(?P<dataset_name>[\w-]+)/files$',
        v.show_files,
        name='show_files'),
    url(r'(?P<dataset_name>[\w-]+)/notifications$',
        v.EditNotificationView.as_view(),
        name='edit_notifications'),
    url(r'(?P<dataset_name>[\w-]+)/check$',
        v.check_dataset,
        name='check_dataset'),
]

