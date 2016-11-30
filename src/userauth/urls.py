from django.conf.urls import url

from .views import login_view, logout_view

urlpatterns = [
    url(r'signin$', login_view, name='signin'),
    url(r'signout$', logout_view, name='signout'),
]
