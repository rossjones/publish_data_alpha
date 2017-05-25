from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf.urls import url, include
from . import views


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.home, name='home'),
    url(r'^cookies$', TemplateView.as_view(template_name='cookies.html'), name='cookies'),
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /\n", content_type="text/plain"), name="robots_file"),
    url(r'^manage/$', views.manage_my_data, name='manage_my_data'),
    url(r'^manage/organisation/$', views.manage_org_data, name='manage_org_data'),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/', include('datasets.urls')),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^api/', include('api.urls')),

    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
