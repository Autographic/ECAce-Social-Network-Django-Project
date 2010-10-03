from django.db import models
from socialnetwork.concordia.constants import *
from socialnetwork.academics import get_current_school_year
from photologue.models import ImageModel
import datetime, random, hashlib

# NOTE: DEPENDENCY ON PROFILE MODULE, IT MUST LOAD FIRST
from socialnetwork.profile.models import *

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
	def __unicode__(self): return self.name.capitalize()

class SchoolYear(models.Model):
	year = models.PositiveSmallIntegerField (
		default = get_current_school_year(),
		help_text = "Nominal value.",
	)
	
	def __unicode__(self):
		return u'School Year %d' % self.year
	
	@classmethod
	def current(cls):
		"Returns the current SchoolYear object."
		return cls.objects.get( year = _get_current_school_year() )

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
	semester_code = models.PositiveSmallIntegerField(
		choices = SEMESTERS,
		help_text = "The name of the semester in the templates is, e.g., {{ course.get_semester_display }}."
	)
	start = models.DateField(
		help_text = "The first day of class.",
	)
	end = models.DateField(
		help_text = "The last day of class.",
	)
	
	
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
	code = models.CharField(
		max_length = 4,
		help_text = "The 4-letter code of the course, e.g. ENCS for ENCS282.",
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
			self.code, self.number, self.name, self.credits,
		)
	
	@property
	def course_code(self):
		return u"%s %d"% ( self.code,self.number )
	
	@property
	def slug(self):
		return u"%s%d"% ( self.code,self.number )
	
	@property
	def sections_by_semester(self):
		secs = self.sections.order_by("-year","-semester")
	
	@classmethod
	def get_course(cls, code, number, year):
		# Will raise DoesNotExist (correctly!) if a nonexistent course, or one not offered this year, is requested.
		# We don't have the authority to offer new courses. We just load them in in August for the upcoming year. :-)
		return cls.objects.get(code=code, number=number, year=year )


	
##### Tying together courses, semesters and sections
class CourseSemester(models.Model):
	"Courses offered in given semesters"
	course = models.ForeignKey ( Course, )
	semester = models.ForeignKey ( Semester, )
	# lecture_sections ->
	
	def __unicode__(self):
		return "%s (%s)" % ( self.course, self.semester, )


from constants import ATTENDANCE_KEY_LENGTH, ATTENDANCE_KEY_LETTERS


##### Sections are sets of students taking a course from a professor, etc.
class LectureSection(models.Model): 
	course_semester = models.ForeignKey ( CourseSemester,
		related_name = "lecture_sections",
	)
	specifier = models.CharField (
		max_length = 2,
		help_text = "The letter (or two) that designates one section from another.",
	)
	classroom = models.ManyToManyField ( Classroom,
		related_name = "lectures",
		help_text = "The room this class is located in.",
	)
	professor = models.ForeignKey ( Professor,
		blank = True, null = True,
		related_name = "lectures",
		help_text = "The professor. You know, the person at the front saying, 'Anyone? Bueller?'",
	)
	# lab_sections ->
	# tutorial_sections ->
	def __unicode__(self): return u'%s %s' % ( self.course_semester, self.specifier, )
	

class LabSection(models.Model): 
	lecture_section = models.ForeignKey ( LectureSection, 
		related_name = "lab_sections",
	)
	specifier = models.CharField (
		max_length = 2,
		help_text = "The letter (or two) that designates one section from another.",
	)
	classroom = models.ManyToManyField ( Classroom,
		related_name = "labs",
		help_text = "The room this class is located in.",
	)
	teaching_assistant = models.ForeignKey ( TeachingAssistant,
		blank = True, null = True,
		related_name = "labs",
	)
	def __unicode__(self): return u'%s [%s]' % ( self.lecture_section.course_semester, self.specifier, )

class TutorialSection(models.Model): 
	lecture_section = models.ForeignKey ( LectureSection,
		related_name = "tutorial_sections",
	)
	specifier = models.CharField (
		max_length = 2,
		help_text = "The letter (or two) that designates one section from another.",
	)
	classroom = models.ManyToManyField ( Classroom,
		related_name = "tutorials",
		help_text = "The room this class is located in.",
	)
	teaching_assistant = models.ForeignKey ( TeachingAssistant,
		blank = True, null = True,
		related_name = "tutorials",
	)
	def __unicode__(self): return u'%s [%s]' % ( self.lecture_section.course_semester, self.specifier, )


##### Schedules designate the weekly pattern of classes
class ClassSchedule(models.Model):
	weekday = models.IntegerField (
		choices = WEEKDAYS,
	)
	week_number = models.IntegerField (
		choices = WEEKS,
	)
	start = models.TimeField ()
	end = models.TimeField ()

class LectureSchedule(ClassSchedule):
	section = models.ForeignKey ( LectureSection,
		related_name = 'weekly_lectures'
	)
	enrollment = models.ManyToManyField ( Student,
		related_name = "lectures",
		through = 'LectureAttendance',
	)
	def __unicode__(self): return u'%s %s' % ( self.section.course_semester, )

class LabSchedule(ClassSchedule):
	section = models.OneToOneField ( LabSection,
		related_name = 'weekly_labs',
	)
	enrollment = models.ManyToManyField ( Student,
		related_name = "labs",
		through = 'LabAttendance',
	)
	def __unicode__(self): return u'%s %s' % ( self.section.course_semester, )

class TutorialSchedule(ClassSchedule):
	section = models.OneToOneField ( TutorialSection,
		related_name = 'weekly_tutorials',
	)
	enrollment = models.ManyToManyField ( Student,
		related_name = "tutorials",
		through = 'TutorialAttendance',
	)
	def __unicode__(self): return u'%s %s' % ( self.section.course_semester, )

##### Sessions are individual meetings of a class 
class SessionAttendance(models.Model):
	date = models.DateField ()
	attendance_code = models.CharField (
		max_length = ATTENDANCE_KEY_LENGTH,
		blank = True,
	)
	def get_attendance_code (self):
		"Return the code, generating it if necessary"
		if not self.attendance_code:
			s = []
			for i in range(ATTENDANCE_KEY_LENGTH):
				s.append(random.choice(ATTENDANCE_KEY_LETTERS))
			self.attendance_code = ''.join(s)
			self.save()
		return self.attendance_code
	
	def check_code(self, test_code):
		"Validate a student's class code."
		return test_code == self.get_attendance_code()

class LectureAttendance(SessionAttendance):
	session = models.OneToOneField ( LectureSchedule,
		related_name = 'attendance',
	)
	student = models.ForeignKey ( Student,
		related_name = 'lecture_attendance',
	)
	def __unicode__(self): return u'%s %s' % ( self.session, self.student, )
	

class LabAttendance(SessionAttendance):
	session = models.OneToOneField ( LabSchedule,
		related_name = 'attendance',
	)
	student = models.ForeignKey ( Student,
		related_name = 'lab_attendance',
	)
	def __unicode__(self): return u'%s %s' % ( self.session, self.student, )

class TutorialAttendance(SessionAttendance):
	session = models.OneToOneField ( TutorialSchedule,
		related_name = 'attendance',
	)
	student = models.ForeignKey ( Student,
		related_name = 'tutorial_attendance',
	)
	def __unicode__(self): return u'%s %s' % ( self.session, self.student, )





