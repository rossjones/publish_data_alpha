from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('datasets/includes/form_controls.html')
def form_controls(request, dataset_name):

    page = request.resolver_match.url_name
    state = request.session.get('flow-state')

    if state in ['checking', 'editing']:
        params = {
            'primary_text': 'Save changes',
            'secondary_text': 'Cancel',
            'secondary_link': 'full_dataset',
            'dataset_name': dataset_name,
        }
        if page.startswith('dataset_addfile'):
            params['primary_text'] = 'Save'
    else:
        params = {
            'primary_text': 'Save and continue',
            'secondary_text': 'Skip this step',
            'dataset_name': dataset_name,
        }
        if page == 'dataset_title':
            params['secondary_link'] = 'dataset_licence'
        elif page == 'dataset_licence':
            params['secondary_link'] = 'dataset_location'
        elif page == 'dataset_location':
            params['secondary_link'] = 'dataset_frequency'
        elif page.startswith('dataset_addfile'):
            params['secondary_link'] = 'dataset_adddoc'
        elif page.startswith('dataset_adddoc'):
            params['secondary_link'] = 'publish_dataset'

    return params
