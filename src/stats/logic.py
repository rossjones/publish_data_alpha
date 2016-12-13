from stats.models import OrganisationStatistic


def get_stats(organisation, title):

    return (
        OrganisationStatistic.objects
        .filter(organisation_name=organisation)
        .filter(subject_title=title)
        .order_by("-timestamp","-value")
        .all()[0:3]
    )





