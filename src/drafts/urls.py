from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import drafts.views as v

urlpatterns = [
    url(r'new$', login_required(v.DatasetCreate.as_view()), name='new_dataset'),
    url(r'edit/(?P<dataset_name>[\w-]+)$',
        login_required(v.DatasetFullEditView.as_view()),
        name='edit_dataset_full'),

    url(r'(?P<dataset_name>[\w-]+)/edit$',
        login_required(v.DatasetEditView.as_view()),
        name='edit_dataset'),
    url(r'(?P<dataset_name>[\w-]+)/country$',
        login_required(v.EditCountryView.as_view()),
        name='edit_country'),
    url(r'(?P<dataset_name>[\w-]+)/licence$',
        login_required(v.EditLicenceView.as_view()),
        name='edit_licence'),
    url(r'(?P<dataset_name>[\w-]+)/frequency$',
        login_required(v.EditFrequencyView.as_view()),
        name='edit_frequency'),
    url(r'(?P<dataset_name>[\w-]+)/add$',
        login_required(v.AddFileView.as_view()),
        name='edit_addfile'),
    url(r'(?P<dataset_name>[\w-]+)/files$',
        login_required(v.show_files),
        name='show_files'),
    url(r'(?P<dataset_name>[\w-]+)/notifications$',
        login_required(v.EditNotificationView.as_view()),
        name='edit_notifications'),
    url(r'(?P<dataset_name>[\w-]+)/check$',
        login_required(v.check_dataset),
        name='check_dataset'),

    # Frequency details
    url(r'(?P<dataset_name>[\w-]+)/frequency/weekly$',
        login_required(v.FrequencyWeeklyView.as_view()),
        name='edit_frequency_weekly'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/monthly$',
        login_required(v.FrequencyMonthlyView.as_view()),
        name='edit_frequency_monthly'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/quarterly$',
        login_required(v.FrequencyQuarterlyView.as_view()),
        name='edit_frequency_quarterly'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/annually$',
        login_required(v.FrequencyAnnuallyView.as_view()),
        name='edit_frequency_annually'),
    url(r'(?P<dataset_name>[\w-]+)/frequency/financial-year$',
        login_required(v.FrequencyFinancialYearView.as_view()),
        name='edit_frequency_financial-year'),
]

