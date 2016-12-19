

def get_orgs_for_user(request):
    if not request.user.is_authenticated():
        return []
    return request.session['organisations']


def set_orgs_for_user(request, orgs):
    if request.user.is_authenticated():
        request.session['organisations'] = orgs


def is_user_in_organisation(request, organisation_name):
    for name, _ in get_orgs_for_user(request):
        if name == organisation_name:
            return True
    return False
