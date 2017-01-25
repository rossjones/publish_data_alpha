import json
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand

from datasets.models import Dataset


class Command(BaseCommand):
    help = 'Creates and uploads the data.json file'

    #def add_arguments(self, parser):
    #    parser.add_argument('action', nargs='?', default='')
    #    parser.add_argument('--force', dest='force', action='store_true')


    def handle(self, *args, **options):
        q = Dataset.objects.filter(published=True)

        print("Creating data.json file for {} datasets".format(q.count()))
        for dataset in q.all():
            pass
