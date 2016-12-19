from django.db import models
from django.contrib.auth.models import AbstractUser


class PublishingUser(AbstractUser):
    apikey = models.CharField(max_length=64)
    USERNAME_FIELD = "email"

    def __repr__(self):
        return self.email


PublishingUser._meta.get_field('email')._unique = True
PublishingUser.REQUIRED_FIELDS.remove("email")
PublishingUser.REQUIRED_FIELDS.append("username")
