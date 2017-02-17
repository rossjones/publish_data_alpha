import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class PublishingUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    apikey = models.CharField(max_length=64, null=True, blank=True)
    USERNAME_FIELD = "email"

    def primary_organisation(self):
        return self.organisations.order_by('name').first()

    def __repr__(self):
        return self.email


PublishingUser._meta.get_field('email')._unique = True
PublishingUser.REQUIRED_FIELDS.remove("email")
PublishingUser.REQUIRED_FIELDS.append("username")
