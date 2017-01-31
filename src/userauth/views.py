from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from .forms import SigninForm

import papertrail


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

                papertrail.log(
                    'login',
                    '{} logged in'.format(user.username),
                    data={
                        'username': user.username,
                        'email': user.email
                    },
                    external_key=user.email
                )

                # TODO: Handle next parameter and redirect there...

                return redirect(settings.LOGIN_REDIRECT_URL)
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
