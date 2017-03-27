import datetime
import os
import sys
import logging
import requests
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from datasets.models import Organisation
from datasets.logic import (most_recent_datafile,
                            number_days_for_frequency,
                            is_dataset_overdue)

from tasks.models import Task

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Checks whether datasets are overdue records the result'

    def add_arguments(self, parser):
        parser.add_argument('--organisation', '-o', dest='organisation')


    def process_organisation(self, organisation):
        print('+ Checking overdue datasets for {}'.format(organisation))
        print('    {} datasets'.format(organisation.datasets.count()))
        for dataset in organisation.datasets.all():
            if not dataset.frequency or dataset.frequency in ['never', 'daily']:
                continue

            print(dataset.name + " " + dataset.frequency)
            df = most_recent_datafile(dataset)
            if not df:
                continue

            # If this dataset has an existing task, then skip it.
            task_count = Task.objects.filter(related_object_id=dataset.name,category='update').count()
            if task_count > 0:
                print('- Skipping {}, task exists'.format(dataset.name))
                continue

            if is_dataset_overdue(dataset):
                print('+ Dataset {} is overdue'.format(dataset.name))
                msg = 'Add missing data to {}'.format(dataset.title)
                Task.objects.create(
                    owning_organisation=organisation.name,
                    related_object_id=dataset.name,
                    description=msg,
                    category='update'
                )

    def handle(self, *args, **options):
        org_name = options.get('organisation')

        if not org_name:
            log.error('Overdue checker currently only processes single organisations')
            sys.exit(1)

        try:
            organisation = Organisation.objects.get(name=org_name)
        except Organisation.DoesNotExist:
            log.error('Organisation {} not found'.format(org_name))
            sys.exit(1)

        self.process_organisation(organisation)
