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
	courses = year.courses_this_year.order_by('code','number')
	c['year'] = year
	c['title'] = 'ENCS Course List' 
	c['subtitle'] = "Courses offered for the %s" % year
	return _show_courses(request,courses,c)

def course_by_discipline(request, discipline):
	"ENCS Course listing"
	c = RequestContext(request)
	disc = get_object_or_404(Discipline, code__iexact=discipline )
	year = SchoolYear.current()
	courses = year.courses_this_year.filter(discipline=disc).order_by('code','number')
	c['year'] = year
	c['title'] = 'ENCS Course List' 
	c['subtitle'] = "Courses offered for the %s" % year
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
	c['courses'] = []
	where = 0
	for ct in counts:
		c['courses'].append(counts[where:where+ct])
		where += ct
	return render_to_response('course/index.html', context_instance=c )

