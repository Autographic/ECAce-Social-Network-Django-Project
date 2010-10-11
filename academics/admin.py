from django.contrib import admin
from constants import *
from models import *
from socialnetwork.campus.models import *
from django.contrib import messages

import httplib, HTMLParser

class SemesterAdminOptions(admin.ModelAdmin):
	fields = ( 
		'year','semester_code',
		'start','end', 
		'exam_start','exam_end', 
	)

	list_display = ( 'name','start','exam_end', )
	inlines = []

admin.site.register(Semester, SemesterAdminOptions)

class SemesterInline(admin.TabularInline):
	model = Semester
	fields = (
		'semester_code','start','end','exam_start','exam_end',
	)


class HTMLFetchError( Exception ):pass

def _fetch_HTML(host,path):
	body = ''
	conn = httplib.HTTPConnection(host)
	conn.request('GET',path)
	response = conn.getresponse()
	
	OK = response.status==200
	if OK:
		body = response.read()
	conn.close()
	if not OK:
		raise HTMLFetchError
	return body


class SchoolYearAdminOptions(admin.ModelAdmin):
	fields = [ 'year',	]
	inlines = [ SemesterInline, ]
	actions = [ 'load_courses', ]
	
	def load_courses(self, request, queryset):
		
		def bounce(): return redirect('..')
		
		try:
			body = _fetch_HTML( COURSE_HTML_HOST, COURSE_HTML_PATH)
		except HTMLFetchError:
			messages.add_message(
				request, messages.ERROR, 
				"There was a problem loading the information; no data was found. Is the address of the registrar's page %s?" % COURSE_HTML_URL
			)
			return bounce()
		courseyear = COURSEYEAR_PATTERN.findall(body)
		if not courseyear:
			messages.add_message(
				request, messages.ERROR, 
				"There was a problem loading the information; no course year was found. Has the format of the registrar's page changed?")
		for c in courseyear:
			start, end = c
			year = SchoolYear.nominal_year( year_number=start )
			break # just once.

		coursedata = COURSEDATA_PATTERN.findall(body)
		if not coursedata:
			messages.add_message(
				request, messages.ERROR, 
				"There was a problem loading the information; no course infomation was found. Has the format of the registrar's page changed?")
			return bounce()

		htmlparser = HTMLParser.HTMLParser()
		maxlen = 0 # record the longest data line's size
		year = SchoolYear.current()
	
		for c in coursedata:
			if len(c[2]) > maxlen: maxlen = len(c[2])
		
			code, number, name, credits = c
		
			name = htmlparser.unescape(name)
			disc = Discipline.objects.get( code=code )
		
			try:
				course = Course.objects.get( discipline=disc, number=number )
				course.name = name
				course.credits = credits
				course.save()
			except Course.DoesNotExist:
				Course.objects.create( discipline=disc, number=number, name=name, credits=credits, year=year )
		if not maxlen:
			messages.add_message(
				request, messages.ERROR, 
				"There was a problem loading the information; no course names were found. Has the format of the registrar's page changed?")
			return redirect('/courses/')
	
		messages.add_message(request, messages.SUCCESS, "The registrar's database was successfully loaded!")

	load_courses.short_description = "Load course database from the Registrar."

admin.site.register(SchoolYear, SchoolYearAdminOptions)

admin.site.register(Discipline)
admin.site.register(Course)
admin.site.register(CourseSemester)





