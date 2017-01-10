from django.views.generic import TemplateView
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^cookies$', TemplateView.as_view(template_name='cookies.html'), name='cookies'),
    url(r'manage$', views.manage_data, name='manage_data'),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/',  include('drafts.urls')),
    url(r'^task/',  include('tasks.urls')),
]
