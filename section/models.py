from django.db import models
from socialnetwork.academics import get_current_school_year
import datetime
from constants import *
from socialnetwork.campus.models import *
from socialnetwork.profile.models import *
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





