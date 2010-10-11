from django.db import models
from socialnetwork.academics import get_current_school_year
import datetime
from constants import *
from socialnetwork.campus.models import *

class Discipline(models.Model):
	"An engineering field."
	code = models.CharField ( 
		max_length=4,
		primary_key = True,
		help_text = "Concordia's program code.",
	)
	name = models.CharField (
		max_length = 64,
		help_text = "Which engineering discipline is this?",
	)
	parent = models.ForeignKey ( "self",
		related_name = 'subdisciplines',
		help_text = "Define a tree of disciplines here.",
		null=True, blank=True,
	)
	def __unicode__(self): return self.name

class SchoolYear(models.Model):
	year = models.PositiveSmallIntegerField (
		default = get_current_school_year(),
		help_text = "Nominal value.",
	)
	
	def __unicode__(self):
		return u'School Year %d' % self.year
	
	@classmethod
	def nominal_year(cls, year_number):
		try:
			return cls.objects.get( year = year_number )
		except cls.DoesNotExist: # This will VERY rarely run.
			return cls.objects.create( year = year_number )
		
	@classmethod
	def current(cls):
		"Returns the current SchoolYear object."
		t = datetime.date.today()
		y = int(t.strftime("%Y"))
		m = int(t.strftime("%m"))
		if m < 9: y -= 1 #####################   very simple, until September it says the previous year.
		return cls.nominal_year(y)

	@classmethod
	def upcoming(cls):
		"Returns the next SchoolYear's object, but ONLY after January 1."
		t = datetime.date.today()
		y = int(t.strftime("%Y"))
		m = int(t.strftime("%m"))
		if m >= 9: y += 1 #####################   very simple, after September it says the next year.
		return cls.nominal_year( y )

class Semester(models.Model):
	"""A division of the school year.
	At Concordia each year is divided into the following semesters:
	
	1 = Spring/Summer ( actually TWO semesters )
	2 = Fall
	3 = Fall+Winter ( overlapping 2, then 4 )
	4 = Winter
	
	This is surely bureaucratic genius, managing in only four entries to 
	specify both overlapping values *and* insufficient granularity.
	"""
	year = models.ForeignKey( SchoolYear,
		related_name = 'semesters',
	)
	semester_code = models.PositiveSmallIntegerField( choices = SEMESTERS, )
	start = models.DateField( help_text = "The first day of class.", )
	end = models.DateField(	help_text = "The last day of class.", )
	exam_start = models.DateField(
		help_text = "The first day of final exams.",
		blank = True, null = True,
	)
	exam_end = models.DateField(
		help_text = "The last day of final exams.",
		blank = True, null = True,
	)
	
	@property
	def name(self): return unicode(self)
	
	@property
	def class_week ( self, which_date = datetime.date.today() ):
		"The first week is zero; after, alternating week 1 and 2."
		this_week = which_date.isocalendar()[1]
		start_week = self.start.isocalendar()[1]
		delta = this_week-start_week
		if not delta: return 0 # the first week is week zero
		return 2 - (delta % 2) # then 1, 2, 1, 2...
	
	def __unicode__(self):
		return u'%s %d' % ( self.get_semester_code_display(), self.year.year )



class Course(models.Model):
	year = models.ForeignKey ( SchoolYear,
		related_name = 'courses_this_year',
	)
	semesters = models.ManyToManyField ( Semester,
		through = 'CourseSemester',
		blank = True,
		related_name = "courses",
	)
	discipline = models.ForeignKey( Discipline,
		help_text = "The 4-letter code of the course, e.g. ENCS for ENCS282.",
		related_name = "courses",
	)
	number = models.PositiveSmallIntegerField (
		help_text = "The 3-digit course code, e.g. 282 for ENCS282."
	)
	name = models.CharField (
		max_length = 128, # actual max length is 76 for 2010
		help_text = "The name of the course, e.g. 'Technical Writing and Communication' for ENCS282.",
	)
	credits = models.DecimalField (
		decimal_places = 2, max_digits = 4,
		help_text = "The credit value of the course, e.g. 3 for ENCS282.",
	)
	final_exam_date = models.DateField(
		help_text = "D-Day.",
		blank = True, null = True,
	)
		
	def __unicode__(self):
		return "%s%d: %s [%.2f credits]" % (
			self.discipline.code, self.number, self.name, self.credits,
		)
	
	@property
	def course_code(self):
		return u"%s %d"% ( self.discipline.code,self.number )
	
	@property
	def slug(self):
		return u"%s%d"% ( self.discipline.code,self.number )
	
	@property
	def sections_by_semester(self):
		return self.sections.order_by("-year","-semester")
	
	@classmethod
	def get_course(cls, code, number, year):
		# Will raise DoesNotExist (correctly!) if a nonexistent course, or one not offered this year, is requested.
		# We don't have the authority to offer new courses. We just load them in in August for the upcoming year. :-)
		return cls.objects.get(discipline__code=code, number=number, year=year )


	
##### Tying together courses, semesters and sections
class CourseSemester(models.Model):
	"Courses offered in given semesters"
	course = models.ForeignKey ( Course, 
		related_name = 'semesters_offered',
	)
	semester = models.ForeignKey ( Semester, 
		related_name = 'courses_offered',
	)
	# lecture_sections ->
	
	def __unicode__(self):
		return "%s (%s)" % ( self.course, self.semester, )


