
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #url(r’^$’, HomePageView.as_view(), name=‘home’),
    url(r'^accounts/', include('userauth.urls')),
    url(r'^dataset/',  include('drafts.urls')),
]
