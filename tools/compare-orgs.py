#!/usr/bin/env python
import csv
import requests
import requests_cache
import sys

requests_cache.install_cache('check_cache')

r = requests.get('https://data.gov.uk/api/3/action/organization_list')

existing = set(r.json()['result'])
register = set()
register_cache = {}

missing_from_live = []
missing_from_register = []


#entry-number,entry-timestamp,item-hash,government-organisation,name,website,start-date,end-date
f = open('organisation-register.csv')
reader = csv.DictReader(f)
for row in reader:
    url = row['website']
    slug = url.split('/')[-1]
    if len(row['end-date']) > 0:
        continue

    register.add(slug)
    register_cache[slug] = row

missing_from_register = existing-register
missing_from_live = register - existing

print("{} missing from register".format(len(missing_from_register)))
print("{} missing from live".format(len(missing_from_live)))

if len(sys.argv) == 2 and sys.argv[1].lower() == 'dump':
    print("Organisations potentially missing from DGU")
    for k, v in register_cache.items():
        if k in missing_from_live:
            print("{}\t{}\t{}".format(v['name'], k, v.get('end-date','open')))
