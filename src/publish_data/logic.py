from django.utils.translation import ugettext as _
from drafts.models import Dataset


from ckan_proxy.logic import datasets_for_user

def dataset_list(user):
    """
    For the given user returns a tuple containing total number of datasets
    both draft and published, and the 20 most recent.
    """

    # TODO: This should be organisation specific
    drafts = Dataset.objects.all().order_by("-last_edit_date")[0:20]
    count = Dataset.objects.count()
    for d in drafts:
        d.status = _("draft")


    results = datasets_for_user(user, offset=0, limit=20)
    datasets = []
    for dataset in results['results']:
        dataset['status'] = _('published')
        datasets.append(dataset)

    total = results['count'] + count

    return (total, (list(drafts) + datasets)[0:20],)
