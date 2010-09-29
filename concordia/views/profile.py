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
from socialnetwork.concordia.models import *
from socialnetwork.concordia.forms import *


def view(request, username=None):
	if username is None: # View someone else's profile
		IS_MY_PROFILE = False
		user = request.user
		username = user.username
	else:
		IS_MY_PROFILE = True
		user = get_object_or_404 ( User, username=username )
	
	c = RequestContext(request)
	c['profile_user'] = user
	
	try: c['student'] = user.student
	except AttributeError: pass
	
	try: c['professor'] = user.professor
	except AttributeError: pass
	
	try:
		c['teaching_assistant'] = user.teaching_assistant
		c['ta'] = user.teaching_assistant # an alias for templaters
	except AttributeError: pass
	
	return render_to_response ("profile/view.html", context_instance = c )

def edit (request): raise NotImplementedError
def search (request): raise NotImplementedError

