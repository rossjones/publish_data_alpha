
from .models import Organisation


def organisations_for_user(user):
    return user.organisation_set.all()
