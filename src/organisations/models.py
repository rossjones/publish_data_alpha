import uuid
from django.db import models
from django.conf import settings

class Organisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200, default="", blank=True)
    title = models.CharField(max_length=200, default="", blank=True)
    description = models.TextField()
    abbreviation = models.CharField(max_length=32, default="", null=True, blank=True)

    created = models.DateTimeField(auto_now=True)

    closed = models.BooleanField(default=False)
    replaced_by = models.CharField(max_length=200, default="", blank=True)

    contact_email = models.CharField(max_length=200, default="", blank=True)
    contact_name = models.CharField(max_length=200, default="", blank=True)
    contact_phone = models.CharField(max_length=200, default="", blank=True)
    foi_email = models.CharField(max_length=200, default="", blank=True)
    foi_name = models.CharField(max_length=200, default="", blank=True)
    foi_phone = models.CharField(max_length=200, default="", blank=True)
    foi_web = models.CharField(max_length=200, default="", blank=True)

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title
