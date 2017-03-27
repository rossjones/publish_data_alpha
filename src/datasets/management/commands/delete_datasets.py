import os
import sys

from django.core.management.base import BaseCommand
from datasets.models import Dataset, Datafile

class Command(BaseCommand):
    help = 'Delete datasets and datafiles whose name contains a string'

    def add_arguments(self, parser):
        parser.add_argument(
            "-y",
            "--yes",
            action="store_true",
            dest="confirm",
            default=False
        )
        parser.add_argument("substring")


    def handle(self, *args, **options):
        substring = options['substring']

        datasets_to_delete = Dataset.objects.filter(
            title__contains = substring
        )

        datafiles_to_delete = Datafile.objects.filter(
            name__contains = substring
        )

        print("About to delete %d datasets and %d datafiles matching '%s'" %
              (len(datasets_to_delete), len(datafiles_to_delete), substring)
        )

        if options['confirm']:
            datasets_to_delete.delete()
            datafiles_to_delete.delete()
            print ('Deleted.')
        else:
            print('Aborted. Please use option --yes to confirm deletion')
