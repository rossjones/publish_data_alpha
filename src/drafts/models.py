from django.db import models


class Dataset(models.Model):
    name = models.CharField(max_length=64, default="")
    title = models.CharField(max_length=64)
    description = models.TextField()

    # ogl, inspire, other
    licence = models.CharField(max_length=64)
    licence_other = models.TextField()

