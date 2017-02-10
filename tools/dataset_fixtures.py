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

def get_extra(extras, key):
    for e in extras:
        if e['key'] == key:
            return e['value']
    return ''

def get_type(dataset):
    return ''

def is_harvested(dataset):
    return bool(get_extra(dataset.get('extras'), 'harvest_object_id'))

def get_doc_type(format):
    return format.lower() in ['pdf', 'doc', 'docx']

SOURCE = os.path.abspath('../../data/datasets.jsonl')

resources = []
results = []
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
            'is_harvested': is_harvested(dataset)
        }
    }
    results.append(data)

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




with open('../src/datasets/fixtures/datasets.json', 'w') as f:
    json.dump(results, f)

with open('../src/datasets/fixtures/datafiles.json', 'w') as f:
    json.dump(resources, f)



