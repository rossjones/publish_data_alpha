from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('datasets/includes/form_controls.html')
def form_controls(request, dataset_name):

    page = request.resolver_match.url_name
    state = request.session.get('flow-state')

    if state in ['checking', 'editing']:
        params = {
            'primary_text': 'Change',
            'secondary_text': 'Cancel',
            'secondary_link': 'edit_full_dataset',
            'dataset_name': dataset_name,
        }
    else:
        params = {
            'primary_text': 'Save and continue',
            'secondary_text': 'Skip this step',
            'dataset_name': dataset_name,
        }

    if page not in ['checking', 'editing']:
        if page == 'edit_dataset_title':
            params['secondary_link'] = 'edit_dataset_organisation'
        elif page == 'edit_dataset_organisation':
            params['secondary_link'] = 'edit_dataset_licence'
        elif page == 'edit_dataset_location':
            params['secondary_link'] = 'edit_dataset_frequency'
        elif page.startswith('edit_dataset_addfile'):
            params['secondary_link'] = 'edit_dataset_adddoc'
        elif page.startswith('edit_dataset_adddoc'):
            params['secondary_link'] = 'publish_dataset'

    else:
        if page.startswith('edit_dataset_addfile'):
            params['primary_text'] = 'Save'

    return params
