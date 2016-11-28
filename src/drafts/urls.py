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
]