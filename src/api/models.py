from django.db import models


class Location(models.Model):

    name = models.CharField(max_length=256)
    location_type = models.CharField(max_length=64, null=True)
