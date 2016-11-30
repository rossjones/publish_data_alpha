
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name='home'),
    url(r'manage$', views.manage_data, name='manage_data'),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/',  include('drafts.urls')),
]
