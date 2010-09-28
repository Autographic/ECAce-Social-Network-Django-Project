from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from socialnetwork.concordia.views import signup

urlpatterns = patterns('',
    # Example:
    # (r'^socialnetwork/', include('socialnetwork.foo.urls')),
    url(r'^$', 'socialnetwork.concordia.views.home' ),
    url(r'^accounts/', include('socialnetwork.base.urls_accounts')),

    url(r'^signup/$', signup ),
    #url(r'^signup/personal/$', signup_personal ),
    #url(r'^signup/concordia/$', signup_concordia ),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
