"""ECA Marketing Mailing List Admin"""

from django.contrib import admin
from models import *

class AttachmentHistoryInline(admin.TabularInline):
	model = AttachmentHistory
	related_name = 'parent'
	fields = (
		'attachment',
		'is_public',
		'file_type',
		'name',
	)
class AttachmentAdminOptions(admin.ModelAdmin):
	fieldsets = [
		( 'File Metadata', { 
			'fields': [
				'attachment',
				'is_public',
				'file_type',
				'name',
				'description',
				'release_date',
			],
			'classes':[],
		}),
	]
	list_display = (
		'name','file_type','release_date', 
	)
	list_filter = (
		'release_date', 
		'file_type',
		'is_public',
	)
	search_fields = (
		'slug', 
		'name', 
	)
	inlines = [ AttachmentHistoryInline, ]

admin.site.register(FileAttachment, AttachmentAdminOptions)

admin.site.register(MediaType)
admin.site.register(FileType)
admin.site.register(FileExtension)
admin.site.register(FileIcon)

