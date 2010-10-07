from django.contrib import admin
from constants import *
from models import *
from socialnetwork.campus.models import *

admin.site.register(Discipline)
admin.site.register(SchoolYear)
admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(CourseSemester)


