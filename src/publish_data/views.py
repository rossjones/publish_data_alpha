from django.shortcuts import render


def home(request):
    if request.user.is_authenticated():
        return dashboard(request)
    return render(request, "main.html", {})

def dashboard(request):
    return render(request, "dashboard.html", {})
