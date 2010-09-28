"""ECAce File Attachment App
By MJP, Aug 26 2010
"""
from django.db import models
import photologue
from django.utils.translation import ugettext as _

AMLL = ATTACHMENT_MAX_NAME_LENGTH = 32

class FileIcon(photologue.models.ImageModel):
	"An icon for pretty screen displays"
	def icon(self):
		func = getattr(self, 'get_icon_url', None)
		if func is None:
			return _('An "icon" photo size has not been defined.')
		else:
			if hasattr(self, 'get_absolute_url'):
				return u'<a href="%s"><img src="%s"></a>' % \
					(self.get_absolute_url(), func())
			else:
				return u'<a href="%s"><img src="%s"></a>' % \
					(self.image.url, func())
	icon.short_description = _('Thumbnail')
	icon.allow_tags = True
	name = models.CharField ( 
		max_length = AMLL,
		help_text = "What is it?",
	)
	
	def __unicode__(self): return self.name

class MediaType(models.Model):
	name = models.CharField (
		max_length = AMLL,
	)
	icon = models.OneToOneField ( FileIcon,
		unique = True, # "Explicit is better than implicit"
		related_name = 'media_types',
		help_text = "The display icon",
	)
	documentation = models.TextField (
		blank = True, null=True,
		help_text = "What are the characteristics and practical uses for this type of media file?",
	)
	
	# Related fields
	# file_types -> FileType
	def __unicode__(self): return self.name

class FileType(models.Model):
	media_type = models.ForeignKey ( MediaType,
		related_name = "file_types"
	)
	name = models.CharField (
		max_length = AMLL,
		help_text = "What are these files commonly referred to as?",
	)
	icon = models.OneToOneField ( FileIcon,
		unique = True, # "Explicit is better than implicit"
		related_name = 'file_types',
		help_text = "The display icon",
	)
	documentation = models.TextField (
		blank = True, null=True,
		help_text = "What are the characteristics and practical uses for this file format?",
	)
	
	# Related fields
	# extensions -> FileExtension
	def __unicode__(self): return self.name

class FileExtension(models.Model):
	"A particular file extension, implying a given file type."
	filetype = models.ForeignKey ( FileType,
		related_name = 'extensions',
		help_text = "The actual file type indicated",
	)
	extension = models.CharField(
		max_length = AMLL,
		help_text = "The extension, with period, i.e. '.png','.txt','.pdf'...",
	)
	
	
	@classmethod
	def prepare_extension(cls,ext):
		e = ext.strip() # strips all whitespace from both ends
		assert(len(e)) # ensure useful characters are submitted, or AssertionError
		e = '%s' % e # ensures only ASCII values (Unicode raises a TypeError)
		if '.' != e[0]: # if the extension has no leading period...
			e = '.%s' % e # add it on
		return e
	
	@classmethod
	def type_for_extension(cls, ext):
		return cls.objects.filter(extension=cls.prepare_extension(ext))
	def __unicode__(self): return self.extension

class FileAttachment(models.Model):
	attachment = models.FileField (
		upload_to = 'attachments/%Y/%m/%d/',
		help_text = "Select your file here.",
	)
	file_type = models.ForeignKey ( FileType,
		blank=True, null=True,
		help_text = "The file type is automatically recognized or my be set manually.",
	)
	name = models.CharField (
		max_length = AMLL,
		help_text = "A concise, descriptive title's best.",
	)
	created = models.DateTimeField ( auto_now_add = True, )
	updated = models.DateTimeField ( auto_now = True, )
	description = models.TextField (
		help_text = "Describe away: the length is unlimited. Basic HTML is okay.",
	)
	release_date = models.DateField (
		help_text = "The download will become available to your studentds on this date.",
	)
	is_public = models.BooleanField (
		default = True, # Assuming current versions usually are distrbuted
		help_text = "Deselect this to hide the file from others.",
	)
	
	# Related fields
	# archive -> AttachmentHistory
	
	def archive_now(self):
		"Create a backup in the database"
		self.archive.create(
			attachment = self.attchment,
			name = self.name,
			file_type = self.file_type,
			updated = self.updated,
			description = self.description,
			release_date = self.release_date,
		)
	def __unicode__(self): return self.name

class AttachmentHistory(models.Model):
	"Tracks previous versions of files"
	parent = models.ForeignKey( FileAttachment,
		related_name = "archive",
		help_text = "The current state of the file.",
	)
	attachment = models.FileField (
		upload_to = 'attachments/%Y/%m/%d/',
		help_text = "Attachment backup.",
	)
	is_public = models.BooleanField (
		default = False, # Assuming obsolete versions usually aren't distrbuted
		help_text = "Should the archived file still be visible to others?",
	)
	archive_created = models.DateTimeField ( auto_now_add = True,
		help_text = "When the archive was written.",
	)
	file_type = models.ForeignKey ( FileType,
		blank=True, null=True,
		help_text = "File type backup.",
	)
	name = models.CharField (
		max_length = AMLL,
		help_text = "File name backup.",
	)
	updated = models.DateTimeField (
		help_text = "Update backup.",
	)
	description = models.TextField (
		help_text = "Description backup.",
	)
	release_date = models.DateField (
		help_text = "Release date backup.",
	)
	def __unicode__(self): 
		return "%s [Archived %s]" % ( self.name, self.archive_created, )

