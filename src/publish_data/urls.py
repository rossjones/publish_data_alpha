
from django.conf.urls import url, include
from . import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.home, name='home'),
    url(r'manage$', views.manage_data, name='manage_data'),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/',  include('drafts.urls')),
    url(r'^task/',  include('tasks.urls')),
]
