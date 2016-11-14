
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #url(r’^$’, HomePageView.as_view(), name=‘home’),
    #url(r’^blog/‘, include(‘blog.urls’)),
    #url(r’^user/‘, include(‘user.urls’)),
]
