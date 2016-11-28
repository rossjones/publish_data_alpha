
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name='home'),
    #url(r’^$’, HomePageView.as_view(), name=‘home’),
    url(r'^accounts/', include('userauth.urls')),
]
