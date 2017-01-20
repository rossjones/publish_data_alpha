
from django.db import models
from django.conf import settings


class ConfigProperty(models.Model):

    key = models.CharField(max_length=256)
    value = models.TextField(null=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Properties"
