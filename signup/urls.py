from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^$', signup ),
    url(r'username_check_ajax/(?P<username>\d+)/', username_available ),
    url(r'^account/$', user ),
    url(r'^personal/$', personal ),
    url(r'^profile/$', profile ),
)

