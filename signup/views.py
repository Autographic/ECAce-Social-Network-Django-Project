# -*- coding: UTF-8 -*-
from django.shortcuts import HttpResponse, redirect, render_to_response
from django.shortcuts import Http404, get_list_or_404, get_object_or_404
from django.template import Context, RequestContext, Template, loader
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, Page, InvalidPage, EmptyPage
from django.contrib import auth
from django.contrib import messages
from django.conf import settings
import datetime, re

from socialnetwork.concordia.models import ECAceRegistrationControl
from socialnetwork.profile.models import *
from socialnetwork.profile.forms import *
from socialnetwork.humanity.forms import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def signup(request):
	"Unlock a registration key first"
	if request.user.is_authenticated() and not request.user.is_admin():
		
	c = RequestContext(request)
	if request.method == 'POST':
		form = StudentIDForm(request.POST)
		if form.is_valid():
			sid,name = form.save()
			request.session['student_ID'] = sid
			request.session['family_name'] = name
			messages.add_message( request, messages.SUCCESS,
				_("Welcome! You may now create an account.")
			)
			return redirect('/signup/personal/')
	else:
		form = StudentIDForm()
	c['form'] = form
	c['title'] = "Create ECAce Account"
	return render_to_response('signup/account.html', context_instance=c )

def user(request):
	"Create Django account"
	c = RequestContext(request)
	if request.method=="POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			d = form.cleaned_data
			uid = d['username']
			pw = d['password1']
			ln = request.session['family_name']
			user = User.create_user(username=uid,password='!',last_name=ln)
			user.set_password(pw)
			user.save()
			auth.login(request,user)
			messages.add_message( request, messages.SUCCESS,
				_("Welcome! You may now create an account.")
			)
			return redirect('/signup/profile/')
	else:
		form = UserCreationForm()
	
	return render_to_response( 'signup/user.html', context_instance=c )

def personal(request):
	"Create HumanBeing stuff"
	c = RequestContext(request)
	if request.method == 'POST':
		form = HumanBeingForm(request.POST)
		if form.is_valid():
			request.session['whoami'] = form.save()
			return redirect('/signup/profile/')
	else:
		form = HumanBeingForm()
	c['form'] = form
	c['title'] = "Create Personal Information"
	return render_to_response('signup/personal.html', context_instance=c )

def profile(request):
	"Create Concordian profile"
	c = RequestContext(request)
	if request.method == 'POST':
		form = ConcordianForm(request.POST)
		if form.is_valid():
			concordian = form.save()
			concordian.user = request.user
			concordian.whoami = request.session['whoami']
			concordian.save()
			return redirect('/profile/edit/')
	else:
		form = ConcordianForm()
	c['form'] = form
	c['title'] = "Create Profile Information"
	return render_to_response('signup/new_profile.html', context_instance=c )

