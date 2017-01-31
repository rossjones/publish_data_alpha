import datetime
import os
import json


def get_extra(extras, key):
    for e in extras:
        if e['key'] == key:
            return e['value']
    return ''

def get_type(dataset):
    return ''

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
            'published_date': dataset.get('medadata_created')
        }
    }
    results.append(data)

    for r in dataset.get('resources',[]):
        f = {
            'model': 'datasets.datafile',
            'pk': r['id'],
            'fields': {
                'title': r.get('description', '')[0:64],
                'url': r.get('url'),
                'format': r.get('format'),
                'dataset_id': dataset['id'],
                # start_date = models.DateField(blank=True, null=True)
                # end_date = models.DateField(blank=True, null=True)
                # month = models.IntegerField(blank=True, null=True)
                # year = models.IntegerField(blank=True, null=True)
                # quarter = models.IntegerField(blank=True, null=True)
                'is_documentation': get_doc_type(r.get('format'))

            }
        }
        resources.append(f)




with open('../src/datasets/fixtures/datasets.json', 'w') as f:
    json.dump(results, f)

with open('../src/datasets/fixtures/datafiles.json', 'w') as f:
    json.dump(resources, f)


