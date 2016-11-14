from django.db import models
from django.contrib.auth.models import User, AbstractUser


class PublishingUser(AbstractUser):
    apikey = models.CharField(max_length=64)
