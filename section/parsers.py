"""MyConcordia schedule parsers"""
import re

class NoDateFound(Exception):
	"An exception raised if the parser finds no date information with its pattern scanner."
	pass

class NoCoursesFound(Exception):
	"An exception raised if the parser finds no matching data with its pattern scanner."
	pass

DATELINE = re.compile(r'<p class="cusisheaderdata">(?P<season>Fall|Winter|Summer) +(?P<year>20\d\d)</p>')
FORMAT1_INFOLINE = re.compile(r'''<td class="cusistabledata">(?P<weekday>Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)</td><td class="cusistabledata">(?P<start_time>\d+:\d+)-(?P<stop_time>\d+:\d+)</td><td class="cusistabledata" align=center>(?P<course_code>[A-Z]{4})</td><td class="cusistabledata" align=center>(?P<course_number>\d{3}) / (?P<season_code>\d)</td><td class="cusistabledata" align=center>(?P<class_type>Lec|Tut|Lab) (?P<course_section>[A-Z]+) (?P<tut_lab_section>[A-Z]+)? *</td><td class="cusistabledata">(?P<building_code>[A-Z]+)-(?P<room_number>[-\w\d]+)</td><td class="cusistabledata" align=center>(?P<campus>SGW|LOY)</td><td class="cusistabledata">(?P<professor>[^<]+) *</td></tr>''')


class ScheduleParser(object):
	"""When a student uploads their schedule from MyConcordia,
	this reads the HTML that MyConcordia generates 
	and from that creates the student's semester schedule."""
	
	invalid_requests = []
	
	def __init__(self,request):
		self.request = request
		self.student = Student.get_from_request(request)
		self.filename = request.FILES['schedule_file'].name
		self.file_data = request.FILES['schedule_file'].read()
		
		semester,year = DATELINE.findall(self.file_data)
		if not year or not semester: raise NoDateFound
		self.year = int(year)
		self.semester = semester_code(semester) # delegates to ecace.constants.semester_code()
		
		# Only the small tabular format supported now, nice the other's a POS
		return self.parse_format_1()
		

	def parse_format_2(self):
		raise NotImplementedErrror
			
	
	def parse_format_1(self):
		"For the logged in student, update their schedule as per the uploaded HTML schedule, format #1 (compact list)."
		student = self.student
		
		data = self.file_data
		
		courses = FORMAT1_INFOLINE.findall(data)
		if not courses: raise NoCoursesFound
		
		courses_added = 0
		labs_added = 0
		tutorials_added = 0
		
		for course_data in courses:
			if 'Lec'==class_type:
				self.register_lecture ( student, course_data )
				courses_added += 1
				continue
			if 'Lab'==class_type:
				self.register_lab ( student, course_data )
				labs_added += 1
				continue
			if 'Tut'==class_type:
				self.register_tutorial ( student, course_data )
				tutorials_added += 1
				continue
			# Huh? An invalid course type. Shouldn't happen anyway due to regex construction.
			self.notify_course_error ( request, course_data, "Invalid class type %s!" % class_type )
		
		return {
			'courses_added': courses_added,
			'labs_added': labs_added,
			'tutorials_added': tutorials_added,
		}
	
	def parse_format_2(request):
		"For the logged in student, update their schedule as per the uploaded HTML schedule, format #2 (visual schedule)."
		# TODO: create extraction formats for the other schedule fomat too.
		raise NotImplementedError
	
	def notify_course_error ( self, course_data, error_msg ):
		messages.add_message( self.request, messages.ERROR, error_msg )
		self.invalid_requests.append(course_data)
		# TODO: log the erroneous course data
	
	def register_lecture( self, student, course_data ):
		# unpack the course data
		( weekday, start_time, stop_time,
			course_code, course_number, season_code,
			class_type, course_section, tut_lab_section,
			building_code, room_number, campus, professor ) = course_data
		
		session = CourseSectionSession.get_session (
			code = course_code, number = course_number, 
			semester = self.semester, year = self.year, specifier = course_section, 
			start_time = start_time, finish_time = finish_time )
		
		try: session.students.add(student)
		except DoesNotExist: # bad course data!
			self.notify_course_error( course_data,
				"Sorry, I couldn't find the course %s %s." % ( course_code, course_number ) 
			)
	
	def register_lab(self,student,year,semester,course_data):
		# unpack the course data
		( weekday, start_time, stop_time,
			course_code, course_number, season_code,
			class_type, course_section, tut_lab_section,
			building_code, room_number, campus, professor ) = course_data
		
		session = LabSectionSession.get_session (
			code = course_code, number = course_number, 
			semester = self.semester, year = self.year, 
			course_specifier = course_section, specifier = tut_lab_section, 
			weekday = weekday, start_time = start_time, finish_time = finish_time )
		
		try: session.students.add(student)
		except DoesNotExist: # bad course data!
			self.notify_course_error( course_data,
				"Sorry, I couldn't find the course %s %s." % ( course_code, course_number ) 
			)
	
	def register_tutorial(self,request,student,year,semester,course_data):
		# unpack the course data
		( weekday, start_time, stop_time,
			course_code, course_number, season_code,
			class_type, course_section, tut_lab_section,
			building_code, room_number, campus, professor ) = course_data
		
		session = TutorialSectionSession.get_session (
			code = course_code, number = course_number, 
			semester = self.semester, year = self.year, 
			course_specifier = course_section, specifier = tut_lab_section, 
			weekday = weekday, start_time = start_time, finish_time = finish_time )
		
		try: session.students.add(student)
		except DoesNotExist: # bad course data!
			self.notify_course_error( course_data,
				"Sorry, I couldn't find the course %s %s." % ( course_code, course_number ) 
			)

		
	def classinfo(
			weekday,start_time,stop_time,
			course_code,course_number,season_code,
			class_type,course_section,tut_lab_section,
			building_code,room_number,campus,
			professor='T.B.A.' ):
		"Prints a class record or returns the data as a dictionary."
		weekday = weekday_lookup(weekday)
		room_number = room_number.strip('-')
		professor = professor.strip()
		if professor=='T.B.A.': professor=None
		else:
			ln,fn = professor.split(', ')
			professor_family_name = ' '.join([ n.capitalize() for n in ln.split(' ')])
			professor_given_name = ' '.join([ n.capitalize() for n in fn.split(' ')])
			professor = "%s %s" % (professor_given_name, professor_family_name)
		
		return locals() # return a dictionary of the unpacked values
		# print the info
		print """
		On %(weekday)s from %(start_time)s to %(stop_time)s, 
		in %(campus)s %(building_code)s%(room_number)s,
		you have %(course_code)s %(course_number)s [%(class_type)s sec.%(course_section)s %(tut_lab_section)s ]
		with %(professor)s.
		""" % locals()

