from django.core.urlresolvers import resolve, Resolver404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from .forms import SigninForm

from runtime_config.audit import audit_log


def login_view(request):
    login_failed = False

    form = SigninForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)

                audit_log(
                    'login',
                    '{} logged in'.format(user.username),
                    data={
                        'username': user.username,
                        'email': user.email
                    },
                    external_key=user.email
                )

                # Before assuming that ?next is valid to redirect
                # to after login, check it. If not valid, just
                # redirect as usual
                redirect_to = settings.LOGIN_REDIRECT_URL
                next_url = request.POST.get('next', '')
                if next_url:
                    try:
                        resolve(next_url)
                        redirect_to = next_url
                    except Resolver404:
                        pass


                return redirect(redirect_to)
            else:
                login_failed = True

    return render(request, "userauth/signin.html", {
        'form': form,
        'login_failed': login_failed,
        'next': request.GET.get('next', '')
    })


def logout_view(request):
    """ Logs out the user and clears the session """
    logout(request)
    return redirect("/")


def user_view(request, username):
    return render(request, "userauth/user.html")
