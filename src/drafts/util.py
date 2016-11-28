from django.utils.text import slugify

from drafts.models import Dataset
from ckan_proxy.logic import show_dataset

def convert_to_slug(title):
    """ Checks for a local dataset with this name, and if not
    found also checks the CKAN install to make sure it isn't in use """
    t = title

    slug = None
    counter = 1

    while True:
        slug = slugify(t)

        draft, dataset = None, None

        try:
            draft = Dataset.objects.get(name=slug)
        except Dataset.DoesNotExist:
            dataset = show_dataset(slug)

        if not draft and not dataset:
            break

        t = "{}{}".format(title, counter)
        counter += 1


    return slug
