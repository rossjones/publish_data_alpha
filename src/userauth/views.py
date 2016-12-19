from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from ckan_proxy.logic import organization_list_for_user
from userauth.logic import set_orgs_for_user
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

                refined_orgs = [(org['name'], org['title'],)
                                for org in organization_list_for_user(user)]
                set_orgs_for_user(request, refined_orgs)

                return redirect("/")
            else:
                login_failed = True

    return render(request, "userauth/signin.html", {
        "form": form,
        "login_failed": login_failed
    })


def logout_view(request):
    """ Logs out the user and clears the session """
    logout(request)
    return redirect("/")
