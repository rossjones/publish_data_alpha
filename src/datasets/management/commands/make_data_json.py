import json
import os
import sys
import tempfile

from django.conf import settings
from django.core.management.base import BaseCommand

from datasets.models import Dataset


class Command(BaseCommand):
    help = 'Creates and uploads the data.json file'

    # def add_arguments(self, parser):
    #    parser.add_argument('action', nargs='?', default='')
    #    parser.add_argument('--force', dest='force', action='store_true')

    def print_head(self, f):
        f.write('''
{
  "@context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
  "@type": "dcat:Catalog",
  "conformsTo": "https://project-open-data.cio.gov/v1.1/schema",
  "describedBy": "https://project-open-data.cio.gov/v1.1/schema/catalog.json",
  "dataset": [
        '''.strip())

    def print_foot(self, f):
        f.write('\n]}')

    # Temporary use until we get properly licence id-> url handling
    def license_for_id(self, id):
        if id == 'uk-ogl':
            return 'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'
        return ''

    def process_dataset(self, dataset):
        d = {
            '@type': 'dcat:Dataset',
            'identifier': '',
            'title': '',
            'description': '',
            'keyword': [],
            'issued': "2016-05-04T10:56:04.000Z",
            'modified': "2016-08-12T19:25:20.565Z",
            'publisher': {
                'name': dataset.organisation.title
            },
            'accessLevel': 'public',
            'distribution': [],
            'license': self.license_for_id(dataset.licence),
            #'contactPoint': {
            #    @type: "vcard:Contact",
            #    fn: "David Brown",
            #    hasEmail: "mailto:"
            #},

        }

        for file in dataset.files.all():
            d['distribution'].append({
                '@type': 'dcat:Distribution',
                'name': file.name,
                'accessURL': file.url,
                #'format': "Web page",
                #'mediaType': file.format,
            })

        return d

    def handle(self, *args, **options):
        q = Dataset.objects.filter(published=True)
        total = q.count()

        print("Creating data.json file for {} datasets".format(total))

        tmp, path = tempfile.mkstemp(suffix='.json')
        os.close(tmp)

        with open(path, 'w') as f:

            self.print_head(f)
            for dataset in q.all():
                processed = self.process_dataset(dataset)
                d = json.dumps(processed, indent=4)
                f.write("  ")
                f.write(d)

                total -= 1
                if total != 0:
                    f.write(",\n")

            self.print_foot(f)

        # TODO: Upload 'path' to known location on S3

        os.unlink(path)
