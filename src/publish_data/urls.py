
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^cookies$', views.cookies, name='cookies'),
    url(r'manage$', views.manage_data, name='manage_data'),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/',  include('datasets.urls')),
    url(r'^task/',  include('tasks.urls')),
]
