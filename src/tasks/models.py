import requests

from django.utils.translation import ugettext as _
from django.conf import settings

from django.db import models

TASK_CATEGORIES = (
    ("update",   _("Update datasets"), ),
    ("fix",      _("Fix datasets"), )
)


class Task(models.Model):
    """ Represents a task that should be completed by an organisation.
    All users who have the reuquired permission will see the task, and
    those that choose to Skip it will not be shown it on future requests.
    """
    # The short name of the owning organisation.
    owning_organisation = models.CharField(max_length=128)

    related_object_id = models.CharField(max_length=200, blank=True, null=True)

    # Used to represent how many broken links, how many days late etc.
    quantity = models.IntegerField(default=0)

    # The name of the permission required to execute this task
    # Users should not be shown the tasks where they don't have
    # the required permission.
    required_permission_name = models.CharField(
        max_length=128,
        default="",
        blank=True
    )

    description = models.TextField()
    category = models.CharField(max_length=20, choices=TASK_CATEGORIES)

    def label_text(self):
        """ The info label to display about a task """
        if self.category == "update":
            return _("Overdue")
        return _("")

