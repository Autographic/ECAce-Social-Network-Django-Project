from django.db import models

from humanity.models import HumanBeing
from academics.models import *
from store.models import TeeShirtSize
from django.contrib.auth.models import User
from photologue.models import ImageModel

from constants import *

class Concordian (models.Model):
	"Custom user-level data"
	user = models.OneToOneField( User, 
		null=True, # for pre-creating Student objects
		related_name = "profile",
	)
	whoami = models.OneToOneField ( HumanBeing,
		null=True, # for pre-creating Student objects
		related_name = "profile",
	)
	whoami.verbose_name_plural = 'whoarewe'
		
	# Profile fields
	motd = models.CharField (
		max_length = 140,
		help_text = "Message of the day: Tweet length (140 characters).",
		blank = True,
	)
	motd.verbose_name = 'MOTD'
	motd.verbose_name_plural = 'MOTDen'
	about_me = models.TextField (
		help_text = "Unlimited length, basic HTML allowed.",
		blank = True,
	)
	interested_in = models.ManyToManyField ( Discipline,
		related_name = 'interested_users',
		null = True, blank = True,
		help_text = "What engineering fields interest you?",
	)
	network = models.ManyToManyField ("self",
		blank = True,
	)
	t_shirt_size = models.ForeignKey ( TeeShirtSize,
		blank = True, null=True,
		help_text = "Optional. But if you fill this in we can automatically choose your size from The Store, and maybe you'll get a surprise gift from a secret admirier!",
	)
	hometown = models.CharField (
		max_length = 128,
		blank = True,
		help_text = "Optional. Whare are you from?",
	)
	"Concordian API definition"
	@property
	def get_student(self):
		"Returns the studentitious profile, or None."
		try: 
			return self.student
		except AttributeError: 
			return None
	@property
	def get_professor(self):
		"Returns the professorial profile, or None."
		try:
			return self.professor
		except AttributeError:
			return None
	@property
	def get_teaching_assistant(self):
		"Returns the TA profile, or None."
		try:
			return self.teaching_assistant
		except AttributeError: 
			return None
	@property
	def get_eca_role(self):
		"Returns the student's ECA role, or None."
		try: 
			return self.eca_role
		except AttributeError: 
			return None
	
	def __unicode__(self): return unicode(self.whoami)

class Student(models.Model):
	concordian = models.OneToOneField ( Concordian,
		related_name = "student",
	)
	# TODO: Should we store a crypto hash instead?
	student_id = models.IntegerField (
		unique = True,
		help_text = "Required. Only Concordia ENCS students may register. We will not disclose this.",
	)
	program = models.CharField (
		max_length = 4,
		choices = ENCS_PROGRAMS,
		help_text = "Which program are you enrolled in?",
		blank=True,
	)
	program_year = models.PositiveSmallIntegerField (
		null = True, blank = True,
		choices = PROGRAM_YEARS,
		help_text = "Which year of your program are you in?",
	)
	last_year_registered = models.PositiveIntegerField (
		null = True, blank = True,
		help_text = "This school year -- assuming you're registered!",
	)
	def __unicode__(self): return unicode(self.concordian.whoami)

class Professor(models.Model):
	concordian = models.OneToOneField ( Concordian,
		related_name = "professor",
	)
	program = models.CharField (
		max_length = 4,
		choices = ENCS_PROGRAMS,
		help_text = "Which program do you teach in?",
		blank=True,
	)
	def __unicode__(self): return unicode(self.concordian.whoami)

class TeachingAssistant(models.Model):
	concordian = models.OneToOneField ( Concordian,
		related_name = "teaching_assistant",
	)
	program = models.CharField (
		max_length = 4,
		choices = ENCS_PROGRAMS,
		help_text = "Which program do you teach in?",
		blank=True,
	)
	def __unicode__(self): return unicode(self.concordian.whoami)


##### Profile extensions
class AssociationStaff(models.Model):
	"An ECA official"
	student = models.OneToOneField ( Student,
		related_name = "eca_role",
		help_text = "The student holding this role.",
	)
	role = models.CharField (
		max_length = 32,
		help_text = "Your role in the ECA."
	)
	class Meta:
		verbose_name_plural = verbose_name = "ECA Staff"
	
	# String representation
	def __unicode__(self):
		name = self.student.concordian.whoami.sorting_name
		return u'%s (%s)'% ( name, self.role, )


##### Profile enhancements
class Avatar(ImageModel):
	profile = models.ForeignKey ( Concordian,
	)
	caption = models.CharField (
		max_length = 256,
		blank = True,
	)
	active = models.BooleanField ( 
		default = True,
		help_text = "Deselect this to make your picture private.",
	)

