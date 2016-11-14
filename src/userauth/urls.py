from django.conf.urls import url

from .views import login_view

urlpatterns = [
    url(r'signin$', login_view, name='signin'),
]