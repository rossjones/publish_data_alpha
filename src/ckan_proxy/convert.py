"""
Provides functions for converting between the local Draft database model
(called a Dataset) and the remote CKAN object (called a package).
"""


def datafile_to_resource(datafile):
    return {
        "description": datafile.title,
        "url": datafile.url
    }


def draft_to_ckan(draft):
    # TODO: Licence other
    # TODO: Creator_user_id (wants an id)
    return {
        "name": draft.name,
        "title": draft.title,
        "notes": draft.description,
        "owner_org": draft.organisation,
        "resources": [datafile_to_resource(r) for r in draft.files.all()],
        "license_id": draft.licence,
        "update_frequency": draft.frequency,
        "geographic_coverage": draft.countries_as_list(),
        "extras": [
            {
                "key": "notifications",
                "value": draft.notifications
            }
        ]
    }


def ckan_to_draft(ckan):
    pass
