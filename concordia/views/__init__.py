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


def home(request):
	"ECAce Home Page"
	c = RequestContext(request)
	c['title'] = 'Welcome to ECAce!'
	c['subtitle'] = "The ECA's New Academically-Oriented Social Network"
	return render_to_response('home.html', context_instance=c )

