from django.conf.urls.defaults import *

import views
from socialnetwork.concordia.views import signup

urlpatterns = patterns('',
    # Example:
    # (r'^socialnetwork/', include('socialnetwork.foo.urls')),
    url(r'username_check_ajax/(?P<username>\d+)/', views.username_available ),
    url(r'^$', views.login ),
    url(r'^login/', views.login ),
    url(r'^logout/$', views.logout ),
    url(r'^logout_verification/$', views.logout_verification ),
    url(r'^signup/', signup ),
)
