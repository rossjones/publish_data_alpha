from django.db import models

class OrganisationStatistic(models.Model):
    organisation_name = models.CharField(max_length=64)
    dataset_title = models.CharField(max_length=256)
    subject_title = models.CharField(max_length=64, default="Downloads")
    value = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    direction = models.CharField(max_length=4)
    since = models.CharField(max_length=20)
