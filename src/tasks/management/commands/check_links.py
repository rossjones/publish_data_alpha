import datetime
import os
import sys
import logging
import requests
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from datasets.models import Organisation
from tasks.models import Task

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Checks whether links are broken and records the result'

    def add_arguments(self, parser):
        parser.add_argument('--organisation', '-o', dest='organisation')


    def link_ok(self, url):
        ok = False

        # Wait a little bit.
        time.sleep(0.5)

        try:
            r = requests.head(url, timeout=(3.0, 3.0,), verify=False)
            ok = (r.status_code != 404)
        except Exception as e:
            print(str(e))
            ok = False

        return ok


    def process_organisation(self, organisation):
        print('+ Checking links for {}'.format(organisation))
        print('    {} datasets'.format(organisation.datasets.count()))
        for dataset in organisation.datasets.all():
            if dataset.files.count() == 0:
                print('- Skipping {}, no resources'.format(dataset.name))
                continue
            print('+ Dataset {} has {} links'.format(dataset.name, dataset.files.count()))

            # If this dataset has an existing task, then skip it.
            task_count = Task.objects.filter(related_object_id=dataset.name).count()
            if task_count > 0:
                print('- Skipping {}, task exists'.format(dataset.name))
                continue

            # If this dataset has ANY broken links, we need to flag it.
            failed = []
            for file in dataset.files.all():
                if not self.link_ok(file.url):
                    failed.append(file)

            if failed:
                print('+ Dataset {} has errors'.format(dataset.name))
                plural = 's' if len(failed) > 1 else ''
                msg = "Replace broken link{} in '{}'".format(plural, dataset.title)
                print(len(str(dataset.id)))
                Task.objects.create(
                    owning_organisation=organisation.name,
                    related_object_id=dataset.name,
                    description=msg,
                    category='fix'
                )
                for file in failed:
                    file.is_broken = True
                    file.last_check = datetime.datetime.now()
                    file.save()


    def handle(self, *args, **options):
        org_name = options.get('organisation')

        if not org_name:
            log.error('Link checker currently only processes single organisations')
            sys.exit(1)

        try:
            organisation = Organisation.objects.get(name=org_name)
        except Organisation.DoesNotExist:
            log.error('Organisation {} not found'.format(org_name))
            sys.exit(1)

        self.process_organisation(organisation)
