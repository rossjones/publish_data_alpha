from django.views.generic import TemplateView
from django.conf.urls import url, include
from . import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.home, name='home'),
    url(r'^cookies$', TemplateView.as_view(template_name='cookies.html'), name='cookies'),
    url(r'manage$', views.manage_data, name='manage_data'),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/',  include('datasets.urls')),
    url(r'^tasks/',  include('tasks.urls')),
    url(r'^api/',  include('api.urls')),

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
