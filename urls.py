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
    
    url(r'^profile/$', 'concordia.views.profile.view'),
    url(r'^profile/view/(?P<username>[^/]+)/$', 'concordia.views.profile.view'),
    url(r'^profile/search/$', 'concordia.views.profile.search'),
    url(r'^profile/edit/$', 'concordia.views.profile.edit'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
