from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from socialnetwork.concordia.views import *

urlpatterns = patterns('',
    url(r'^$', 'socialnetwork.concordia.views.home' ),
    url(r'^accounts/', include('socialnetwork.base.urls_accounts')),

    url(r'^signup/$', signup_account ),
    url(r'^signup/personal/$', signup_personal ),
    url(r'^signup/concordia/$', signup_concordia ),
    
    url(r'^profile/$', 'concordia.views.profile_view'),
    url(r'^profile/view/(?P<username>[^/]+)/$', 'concordia.views.profile_view'),
    url(r'^profile/search/$', 'concordia.views.profile_search'),
    url(r'^profile/edit/$', 'concordia.views.profile_edit'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
