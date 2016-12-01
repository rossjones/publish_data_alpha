from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    if request.user.is_authenticated():
        return dashboard(request)
    return render(request, "home.html", {})

def dashboard(request):
    return render(request, "dashboard.html", {})

@login_required()
def manage_data(request):
    # TODO: Determine default sort order, most recent first with drafts
    # and published interspersed? Paging the remote datasets will be a
    # pain
    return render(request, "manage.html", {})
