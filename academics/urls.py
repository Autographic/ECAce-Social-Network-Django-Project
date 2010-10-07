from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^', course_index),
    url(r'(?P<discipline>[A-Z]{4})/^', course_by_discipline),
)

