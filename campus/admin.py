from django.contrib import admin
from models import *

class CampusBuildings(admin.TabularInline):
	model = Building
class CampusAdmin(admin.ModelAdmin):
	inlines = ( CampusBuildings, )

class BuildingClassrooms(admin.TabularInline):
	model = Classroom
class BuildingAdmin(admin.ModelAdmin):
	inlines = ( BuildingClassrooms, )

admin.site.register(Campus, CampusAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Classroom)

