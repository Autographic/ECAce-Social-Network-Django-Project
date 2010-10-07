from django.conf.urls.defaults import *

import views
#from socialnetwork.concordia.views import signup

urlpatterns = patterns('',
    url(r'^$', views.login ),
    url(r'^login/', views.login ),
    url(r'^logout/$', views.logout ),
    url(r'^logout_verification/$', views.logout_verification ),
)
