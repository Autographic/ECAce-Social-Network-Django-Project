from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^accounts/', include('socialnetwork.base.urls')),
    url(r'^signup/', include('socialnetwork.signup.urls')),
    url(r'^profile/', include('socialnetwork.profile.urls')),
    url(r'^course/', include('socialnetwork.academics.urls')),
    #url(r'^store/', include('socialnetwork.profile.urls')),
    
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

