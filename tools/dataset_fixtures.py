import uuid
from calendar import monthrange
from datetime import datetime

import datetime
import os
import json

def calculate_dates_for_month(month, year):
    (_, e,) = monthrange(year, month)
    return (
        datetime.datetime(year=year, month=month, day=1),
        datetime.datetime(year=year, month=month, day=e)
    )

def calculate_dates_for_year(year):
    return (
        datetime.datetime(year=year, month=1, day=1),
        datetime.datetime(year=year, month=12, day=31)
    )

def convert_frequency(freq):
    if not freq:
        return ''

    return {
        'annual': 'annually',
        'quarterly': 'quarterly',
        'monthly': 'monthly'
    }.get(freq, 'never')


def get_extra(extras, key):
    for e in extras:
        if e['key'] == key:
            return e['value']
    return ''

def get_type(dataset):
    if get_extra(dataset['extras'], 'UKLP') == 'True':
        return 'inspire'
    return ''

def is_harvested(dataset):
    return bool(get_extra(dataset.get('extras'), 'harvest_object_id'))

def get_doc_type(format):
    return format.lower() in ['pdf', 'doc', 'docx']

def process_inspire(dataset):
    extras = dataset['extras']
    data = {
        'model': 'datasets.inspiredataset',
        'pk': str(uuid.uuid4()),
        'fields': {
            'dataset_id': dataset['id'],
            'bbox_east_long': get_extra(extras, 'bbox-east-long'),
            'bbox_north_lat': get_extra(extras, 'bbox-north-lat'),
            'bbox_south_lat': get_extra(extras, 'bbox-south-lat'),
            'bbox_west_long': get_extra(extras, 'bbox-west-long'),
            'coupled_resource': get_extra(extras, 'coupled-resource'),
            'dataset_reference_date': get_extra(extras, 'dataset-reference-date'),
            'frequency_of_update': get_extra(extras, 'frequency-of-update'),
            'harvest_object_id': get_extra(extras, 'harvest_object_id'),
            'harvest_source_reference': get_extra(extras, 'harvest_source_reference'),
            'import_source': get_extra(extras, 'import_source'),
            'metadata_date': get_extra(extras, 'metadata-date'),
            'metadata_language': get_extra(extras, 'metadata-language'),
            'provider': get_extra(extras, 'provider'),
            'resource_type': get_extra(extras, 'resource-type'),
            'responsible_party': get_extra(extras, 'responsible-party'),
            'spatial': get_extra(extras, 'spatial'),
            'spatial_data_service_type': get_extra(extras, 'spatial-data-service-type'),
            'spatial_reference_system': get_extra(extras, 'spatial-reference-system'),
        }
    }



    return data

SOURCE = os.path.abspath('../../data/datasets.jsonl')

resources = []
results = []
inspire = []

for line in open(SOURCE, 'r').readlines():
    dataset = json.loads(line)

    notes = dataset.get('notes', '')
    if notes:
        summary = notes[0:140]
    else:
        summary = dataset.get('title')

    data = {
        'model': 'datasets.dataset',
        'pk': dataset['id'],
        'fields': {
            'name': dataset.get('name'),
            'title': dataset.get('title')[0:200],
            'summary': summary,
            'description': notes or '',
            'organisation_id': dataset.get('owner_org'),
            'last_edit_date': dataset.get('metadata_modified'),
            'licence': dataset.get('license_id') or 'no-licence',
            'dataset_type': get_type(dataset),
            'published': True,
            'published_date': dataset.get('medadata_created'),
            'frequency': convert_frequency(dataset.get('update_frequency')),
            'is_harvested': is_harvested(dataset)
        }
    }
    results.append(data)

    if data['fields']['dataset_type'] == 'inspire':
        inspire.append(process_inspire(dataset))


    def get_start_end_date(date_string):
        if not date_string:
            return '', ''

        if len(date_string) == 4:
            return calculate_dates_for_year(int(date_string))

        slash_count = date_string.count('/')
        parts = []
        if slash_count == 2:
            parts = date_string.split('/')[1:]
        elif slash_count == 1:
            parts = date_string.split('/')

        if parts and len(parts) == 2:
            return calculate_dates_for_month(int(parts[0]), int(parts[1]))

        return '', ''

    for r in dataset.get('resources',[]):
        start, end = None, None
        if 'date' in r:
            start, end = get_start_end_date(r['date'])

        f = {
            'model': 'datasets.datafile',
            'pk': r['id'],
            'fields': {
                'title': r.get('description', '')[0:64],
                'url': r.get('url'),
                'format': r.get('format'),
                'dataset_id': dataset['id'],
                'is_documentation': get_doc_type(r.get('format'))
            }
        }
        if start and end:
            f['fields']['start_date'] = start.date().isoformat()
            f['fields']['end_date'] = end.date().isoformat()

        resources.append(f)

with open('../src/datasets/fixtures/inspire.json', 'w') as f:
    json.dump(inspire, f)

with open('../src/datasets/fixtures/datasets.json', 'w') as f:
    json.dump(results, f)

with open('../src/datasets/fixtures/datafiles.json', 'w') as f:
    json.dump(resources, f)



