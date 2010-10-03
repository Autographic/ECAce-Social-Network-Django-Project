from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^$', signup ),
    url(r'^account/$', user ),
    url(r'^personal/$', personal ),
    url(r'^profile/$', profile ),
)

