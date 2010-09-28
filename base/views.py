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
from django.contrib import messages

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.views import login as auth_login


#from models import *
#from forms import *

def username_available(request,username):
	"AJAX username validator"
	c = RequestContext(request)
	try:
		User.objects.get(username=username)
		c['user_available'] = False
	except User.DoesNotExist:
		c['user_available'] = True
	return render_to_response('profile/registration_form.html', context_instance = c )

def login(request):
	return auth_login(request)

def logout(request):
	auth.logout(request)
	return redirect('/accounts/logout_verification/')

def logout_verification(request):
	if request.user.is_authenticated():
		messages.add_message(
			request, messages.ERROR, 
			"There was a problem: You have NOT been logged out." )
	messages.add_message(
		request, messages.INFO, 
		"You have been logged out. See you soon!" )
	return redirect ('/')

