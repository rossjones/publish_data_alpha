from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from .views import login_view, logout_view, user_view
from django.contrib.auth.views import (password_reset,
                                       password_reset_done,
                                       password_reset_confirm,
                                       password_reset_complete)
import userauth.views as v
from userauth.forms import UserPasswordReset

urlpatterns = [
    url(r'signin$', login_view, name='signin'),
    url(r'signout$', logout_view, name='signout'),
    url(r'user/(?P<username>[^/]+)/$',
        login_required(v.user_view),
        name='user'),

    url(r'password_reset/$', password_reset, {
            'template_name': 'userauth/password_reset.html',
            'password_reset_form': UserPasswordReset
        },
        name='password_reset'),

    url(r'password_reset/done/$', password_reset_done, {
            'template_name': 'userauth/password_reset_done.html'
        },
        name='password_reset_done'),

    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, {
            'template_name': 'userauth/password_reset_confirm.html'
        },
        name='password_reset_confirm'),
    url(r'reset/done/$', password_reset_complete, {
            'template_name': 'userauth/password_reset_complete.html'
        },
        name='password_reset_complete'),
]
