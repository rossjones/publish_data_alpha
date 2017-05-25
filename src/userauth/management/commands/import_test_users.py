import json
import os
import sys

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datasets.models import Organisation


class Command(BaseCommand):
    help = 'Imports test users from a json file'

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", dest="filename")

    def handle(self, *args, **options):
        filename = options['filename']

        if Organisation.objects.count() == 0:
            print("Run './manage.py loaddata organisations' first")
            sys.exit(1)

        self.co = Organisation.objects.get(name='cabinet-office')
        self.gps = Organisation.objects.get(
            name='government-procurement-service')
        self.beis = Organisation.objects.get(
            name='department-for-business-energy-and-industrial-strategy')

        if filename:
            if not os.path.exists(filename):
                print("Could not find file {}".format(filename))
            data = json.load(open(filename, "r"))
        else:
            data = json.load(sys.stdin)

        for user_details in data:
            try:
                orgname = user_details.pop('organisation')
                user = get_user_model().objects.get(
                    email=user_details['email']
                )
                print("Not updating existing user")
            except BaseException:
                password = user_details.pop('password')
                user = get_user_model().objects.create(
                    **user_details
                )
                user.set_password(password)
                user.save()

                try:
                    org = Organisation.objects.get(name=orgname)
                    org.users.add(user)
                except BaseException:
                    print("unknown or missing organisation")

                print("User {} created".format(user.email))
