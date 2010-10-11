# -*- coding: UTF-8 -*-
from django.shortcuts import HttpResponse, redirect, render_to_response
from django.shortcuts import Http404, get_list_or_404, get_object_or_404
from django.template import Context, RequestContext, Template, loader
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page, InvalidPage, EmptyPage
from django.contrib import messages
from django.conf import settings
import datetime, re

from django.contrib.auth.models import User
from socialnetwork.humanity.models import HumanBeing, HumanName
from socialnetwork.humanity.forms import HumanBeingForm, HumanNameForm
from models import *
#from forms import *

def course_index(request):
	"ENCS Course listing"
	c = RequestContext(request)
	year = SchoolYear.current()
	courses = Course.objects.filter(year=year).order_by('discipline__code','number')
	c['year'] = year
	c['title'] = 'Full Course List' 
	c['pretitle'] = "Courses offered for %s" % year
	return _show_courses(request,courses,c)

def course_by_discipline(request, discipline):
	"ENCS Course listing"
	c = RequestContext(request)
	disc = get_object_or_404(Discipline, code__iexact=discipline )
	year = SchoolYear.current()
	courses = Course.objects.filter(discipline=disc,year=year).order_by('number')
	c['year'] = year
	c['title'] = '%s Course List' % disc.name
	c['pretitle'] = "Courses offered for %s" % year
	return _show_courses(request,courses,c)

def _show_courses(request,courses,context):
	"ENCS Course listing"
	c = context
	c['course_count'] = ct = courses.count()
	COLUMNS = 4
	length = ct/COLUMNS
	counts = [ length for i in range(COLUMNS) ]
	for i in range(ct%4):
		counts[i] += 1
	columns = []
	where = 0
	for ct in counts:
		batch = courses[where:where+ct]
		columns.append( batch )
		where += ct
	'''
	for col in columns:
		current_discipline = None # Always head columns with headers
		for course in col:
			is_new_section = False
			if not current_discipline or current_discipline != course.discipline:
				current_discipline = course.discipline
				is_new_section = True
			course.annotate( is_new_section = is_new_section )
	'''	
	
	c['disciplines'] = Discipline.objects.order_by('code')
	
	c['columns'] = columns 
	
	return render_to_response('course/index.html', context_instance=c )


def course_view(request, discipline, number):
	"ENCS Course listing"
	c = RequestContext(request)
	disc = get_object_or_404(Discipline, code__iexact=discipline )
	course = get_object_or_404(Course, discipline=disc, number=number )
	c['title'] = course.name
	c['discipline'] = disc
	c['course'] = course
	return render_to_response('course/view.html', context_instance=c )

