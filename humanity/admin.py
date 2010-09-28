from django.contrib import admin

from models import Gender
from models import HumanBeing, HumanName

admin.site.register(Gender)



#class FragInline(admin.TabularInline):
#	model = NameFragment

#class HumanNameAdminOptions(admin.ModelAdmin):
#	fields = ('style','pattern',)
#	inlines = [ FragInline, ]

admin.site.register(HumanName)#, HumanNameAdminOptions)


class NameInline(admin.TabularInline):
	fields = ( 'given', 'middle', 'family', )
	model = HumanName

class HumanBeingAdminOptions(admin.ModelAdmin):
	fields = ( 'gender', 'birthdate', )
	inlines = [ NameInline, ]

admin.site.register(HumanBeing, HumanBeingAdminOptions)

