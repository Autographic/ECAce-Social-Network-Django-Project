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
from forms import *

def home(request):
	"ECAce Home Page"
	c = RequestContext(request)
	c['title'] = 'Welcome to ECAce!'
	c['subtitle'] = "The ECA's New Academically-Oriented Social Network"
	return render_to_response('home.html', context_instance=c )

def signup(request):
	"Create the Django user account"
	c = RequestContext(request)
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.login(request)
			return redirect('/signup/personal/')
	else:
		form = UserCreationForm()
	c['form'] = form
	c['title'] = "Create ECAce Account"
	return render_to_response('/who/knows/where.html', context_instance=c )

def signup_personal(request):
	c = RequestContext(request)
	if request.method == 'POST':
		form = HumanBeingForm(request.POST)
		if form.is_valid():
			request.session.whoami = form.save()
			return redirect('/signup/concordia/')
	else:
		form = HumanBeingForm()
	c['form'] = form
	c['title'] = "Create Personal Information"
	return render_to_response('/who/knows/where.html', context_instance=c )

def signup_concordia(request):
	c = RequestContext(request)
	if request.method == 'POST':
		form = ConcordianForm(request.POST)
		if form.is_valid():
			concordian = form.save()
			concordian.user = request.user
			concordian.whoami = request.session.whoami
			concordian.save()
			return redirect('/profile/edit/')
	else:
		form = ConcordianForm()
	c['form'] = form
	c['title'] = "Create Profile Information"
	return render_to_response('/who/knows/where.html', context_instance=c )


def OLDsignup(request):
	"Starts a member registration by making a user object."
	c = RequestContext(request)
	if request.method == 'POST':
		form1 = ConcordianRegistrationForm( request.POST )
		valid = True
		if form1.is_valid():
			user = form1.save() # The Django user is created
		else:
			valid = False
		form2 = HumanBeingForm( request.POST )
		if form2.is_valid(): # create HumanBeing and basic name data
			person = HumanBeing.people.create(
				gender = form2.cleaned_data['gender'],
				birthdate = form2.cleaned_data['birthdate']
			)
			name = HumanName.objects.create (
				given = form2.cleaned_data['given_name'],
				family = form2.cleaned_data['family_name'],
				name_schema_family_last = form2.cleaned_data['name_schema_family_last'],
				whoami = person,
			)
		else: valid = False
		if not valid:
			messages.add_message(
				request, messages.ERROR, 
				"There was a problem with your data." )
		else:
			form3 = StudentIDForm( request.POST )
			if form3.is_valid(): # Ensures a valid *and* pre-defined user ID
				student = Student.objects.get(student_id=form3.cleaned_data['student_id'])
				if not student.user:
					student.user = user
					student.whoami = person
					student.save()
					messages.add_message(
						request, messages.SUCCESS, 
						"Your profile has been created." )
					return redirect ('/profile/')
				else:
					messages.add_message(
						request, messages.NOTICE, 
						"There's already a profile." )
				return redirect( student.absolute_url() )
	else: # create default forms if no data
		form1 = ConcordianRegistrationForm ()
		form2 = HumanBeingForm()
		form3 = StudentIDForm()
	c['form1'] = form1
	c['form2'] = form2
	c['form3'] = form3
	c['title'] = "Create Account"
	c['subtitle'] = "Welcome to ECAce!"
	return render_to_response('profile/registration_form.html', context_instance = c )
	


