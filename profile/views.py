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

from models import *
from forms import *
from socialnetwork.humanity.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

def view_own(request):
	"Profile viewer"
	return view(request,user=request.user)

def view(request, username=None, user=None ):
	"Profile viewer"
	if username:
		user = User.objects.get(username)
	else:
		assert(user)
		
	raise NotImplementedError

def search(request):
	"Profile search engine"
	raise NotImplementedError

def edit(request):
	"Profile editor page"
	raise NotImplementedError


