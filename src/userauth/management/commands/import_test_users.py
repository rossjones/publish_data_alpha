import json
import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Imports test users from a json file'

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", dest="filename", required=True)

    def handle(self, *args, **options):
        filename = options['filename']
        if not os.path.exists(filename):
            print("Could not find file {}".format(filename))

        data = json.load(open(filename, "r"))

        for user_details in data:

            try:
                user = get_user_model().objects.get(email=user_details['email'])
                print("Not updating existing user")
            except:
                password = user_details.pop('password')
                user = get_user_model().objects.create(
                    **user_details
                )
                user.set_password(password)
                user.save()

                print("User {} created".format(user.email))
