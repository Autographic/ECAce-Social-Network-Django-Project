from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^$', view_own ),
    url(r'^view/(?P<username>[^/]+)/$', view ),
    url(r'^search/$', search ),
    url(r'^edit/$', edit ),
)
