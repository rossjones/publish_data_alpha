from django.conf.urls import url

import drafts.views as v

urlpatterns = [
    url(r'new$', v.DatasetCreate.as_view(), name='new_dataset'),
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

    # Frequency details
    url(r'(?P<dataset_name>[\w-]+)/frequency/weekly$',
        v.FrequencyWeeklyView.as_view(),
        name='edit_frequency_weekly'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/monthly$',
        v.FrequencyMonthlyView.as_view(),
        name='edit_frequency_monthly'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/quarterly$',
        v.FrequencyQuarterlyView.as_view(),
        name='edit_frequency_quarterly'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/annually$',
        v.FrequencyAnnuallyView.as_view(),
        name='edit_frequency_annually'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/financial-year$',
        v.FrequencyFinancialYearView.as_view(),
        name='edit_frequency_financial-year'),
]

