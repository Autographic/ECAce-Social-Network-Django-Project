from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
	# root level handled by a flatpage
    url(r'^index/$', course_index),
    url(r'^(?P<discipline>[A-Z]{3,4})/$', course_by_discipline),
    url(r'^(?P<discipline>[A-Z]{3,4})(?P<number>\d{3})/$', course_view ),
)

