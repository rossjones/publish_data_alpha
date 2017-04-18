import datetime
import os
import json

def get_extra(extras, key):
    for e in extras:
        if e['key'] == key:
            return e['value']
    return ''

SOURCE = os.path.abspath('../../data/organizations.jsonl')

results = []
for line in open(SOURCE, 'r').readlines():
    org = json.loads(line)

    data = {
        'model': 'datasets.organisation',
        'pk': org['id'],
        'fields': {
            'name': org.get('name'),
            'title': org.get('title'),
            'description': org.get('description'),
            'abbreviation': org.get('abbreviation'),
            'closed': org.get('closed', False),
            'replaced_by': str(org.get('replaced_by', '')),
            'created': datetime.datetime.now().isoformat() + '+00:00',
            'contact_email': get_extra(org['extras'], 'contact-email'),
            'contact_name': get_extra(org['extras'], 'contact-name'),
            'contact_phone': get_extra(org['extras'], 'contact-phone'),
            'foi_email': get_extra(org['extras'], 'foi-email'),
            'foi_name': get_extra(org['extras'], 'foi-name'),
            'foi_phone': get_extra(org['extras'], 'foi-phone'),
            'foi_web': get_extra(org['extras'], 'foi-web'),
            'category': org.get('category', '')
        }
    }
    results.append(data)


with open('../src/datasets/fixtures/organisations.json', 'w') as f:
    json.dump(results, f)

    # category =

"""
[
  {
    "model": "tasks.task",
    "pk": 1,
    "fields": {
      "owning_organisation": "cabinet-office",
      "required_permission_name" : "",
      "description": "Improve 'Anti-social behaviour order statistics, England and Wales' by 3 February 2017",
      "category": "improve"
    }
  },
"""
