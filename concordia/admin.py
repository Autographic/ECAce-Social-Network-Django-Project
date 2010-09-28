from django.contrib import admin
from models import *

### Physical Plant
class BuildingClassrooms(admin.TabularInline):
	model = Classroom
class BuildingAdmin(admin.ModelAdmin):
	inlines = ( BuildingClassrooms, )
admin.site.register(Building, BuildingAdmin)
admin.site.register(Classroom)

### Academics
admin.site.register(Discipline)

class SchoolYearSemesters(admin.TabularInline):
	model = Semester
class SchoolYearAdmin(admin.ModelAdmin):
	inlines = ( SchoolYearSemesters, )
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(Semester)

admin.site.register(Course)
admin.site.register(CourseSemester)
#admin.site.register(Section)

class LectureScheduleInline(admin.TabularInline):
	model = LectureSchedule
class LabScheduleInline(admin.TabularInline):
	model = LabSchedule
class TutorialScheduleInline(admin.TabularInline):
	model = TutorialSchedule
class LectureAdmin(admin.ModelAdmin):
	inlines = ( LectureScheduleInline, )
class LabAdmin(admin.ModelAdmin):
	inlines = ( LabScheduleInline, )
class TutorialAdmin(admin.ModelAdmin):
	inlines = ( TutorialScheduleInline, )

admin.site.register(LectureSection, LectureAdmin)
admin.site.register(LabSection, LabAdmin)
admin.site.register(TutorialSection, TutorialAdmin)

class LectureAttendanceInline(admin.TabularInline):
	model = LectureAttendance
class LabAttendanceInline(admin.TabularInline):
	model = LabAttendance
class TutorialAttendanceInline(admin.TabularInline):
	model = TutorialAttendance
class LectureScheduleAdmin(admin.ModelAdmin):
	inlines = ( LectureAttendanceInline, )
class LabScheduleAdmin(admin.ModelAdmin):
	inlines = ( LabAttendanceInline, )
class TutorialScheduleAdmin(admin.ModelAdmin):
	inlines = ( TutorialAttendanceInline, )

admin.site.register(LectureSchedule,LectureScheduleAdmin)
admin.site.register(LabSchedule,LabScheduleAdmin)
admin.site.register(TutorialSchedule,TutorialScheduleAdmin)


admin.site.register(Concordian)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(TeachingAssistant)
admin.site.register(AssociationStaff)
admin.site.register(Avatar)

