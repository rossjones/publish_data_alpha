from django.conf.urls import url

import drafts.views as v

urlpatterns = [
    url(r'new$', v.new_dataset, name='new_dataset'),
    url(r'(?P<dataset_name>[\w-]+)/edit$',
        v.edit_dataset,
        {'form_name': 'title'},
        name='edit_licence'
    ),
    url(r'(?P<dataset_name>[\w-]+)/licence$',
        v.edit_dataset,
        {'form_name': 'licence'},
        name='edit_licence'
    ),
    url(r'(?P<dataset_name>[\w-]+)/theme$',
        v.edit_dataset,
        {'form_name': 'theme'},
        name='edit_theme'),
    url(r'(?P<dataset_name>[\w-]+)/country$',
        v.edit_dataset,
        {'form_name': 'country'},
        name='edit_country'),
    url(r'(?P<dataset_name>[\w-]+)/frequency$',
        v.edit_dataset,
        {'form_name': 'frequency'},
        name='edit_frequency'),
    url(r'(?P<dataset_name>[\w-]+)/add$',
        v.add_file,
        name='edit_addfile'),
    url(r'(?P<dataset_name>[\w-]+)/files$',
        v.show_files,
        name='show_files'),
    url(r'(?P<dataset_name>[\w-]+)/check$',
        v.check_dataset,
        name='check_dataset'),
    url(r'(?P<dataset_name>[\w-]+)/notifications$',
        v.edit_dataset,
        {'form_name': 'notifications'},
        name='edit_notifications'),

]
