from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import SigninForm

def login_view(request):
    login_failed = False

    form = SigninForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                login_failed = True

    return render(request, "userauth/signin.html", {
        "form": form,
        "login_failed": login_failed
    })

def logout_view(request):
    logout(request)
    return redirect("/")
