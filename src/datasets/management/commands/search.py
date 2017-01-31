import json
import os
import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from datasets.models import Dataset
from datasets.search import bulk_import, reset_index

class Command(BaseCommand):
    help = 'Interacts with the configured search index'

    def add_arguments(self, parser):
        parser.add_argument('action', nargs='?', default='')
        parser.add_argument('--force', dest='force', action='store_true')

    def sure(self, options):
        if options['force'] == True:
            return True

        result = input('Are you sure? ')
        if not result:
            return False
        while len(result) < 1 or result[0].lower() not in "yn":
            result = input("Please answer yes or no: ")
        return result[0].lower() == "y"

    def handle(self, *args, **options):
        if not self.sure(options):
            print("Ok, aborting")
            sys.exit(1)

        action = options['action']
        if action == 'reset':
            self.do_reset()
        elif action == 'rebuild':
            self.do_rebuild()
        else:
            print("Unknown command, use rebuild or reset.")


    def do_rebuild(self):
        q = Dataset.objects.filter(published=True)
        count = q.count()

        print("Rebuilding index {} - ({} datasets)".format(
            settings.ES_INDEX,count)
        )

        previous = 0
        for end in range(250, count + 250, 250):
            datasets = q.all()[previous:end]
            print("Indexing from {} to {}".format(previous, end))

            k = [
                {
                "_index": settings.ES_INDEX,
                "_type" : "datasets",
                "_id"   : str(d.id),
                "_source": d.as_dict(),
                } for d in datasets]

            bulk_import(k)
            previous = end



    def do_reset(self):
        print("Resetting index")
        reset_index()
