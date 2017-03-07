from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import login_view, logout_view, user_view
import userauth.views as v

urlpatterns = [
    url(r'signin$', login_view, name='signin'),
    url(r'signout$', logout_view, name='signout'),
    url(r'^user/(?P<username>[^/]+)/$',
        login_required(v.user_view),
        name='user')
]
