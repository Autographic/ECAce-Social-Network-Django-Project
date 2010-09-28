from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from socialnetwork.humanity.models import HumanBeing
from constants import WEIGHTS_COARSE, WEIGHTS_FINE, DEFAULT_WEIGHT
from django.conf import settings

"""	Social Network Base Classes
SocialNetworkSite
Weighted, Metadata
"""

#########
# Created Sep 4 2010 by MJP
#

class SocialNetworkSite (Site):
	"Custom sitewide settings"
	# name, base_url: inherited
	slug = models.CharField (
		max_length = 8,
		unique = True,
		help_text = "A brief string of letters, numbers and underscores under which to store the site's files."
	)
	media_url = models.URLField (
		help_text = "The base URL of the media server.", 
	)
	slogan = models.CharField ( max_length = 128, )






##### Add-on classes for metadata and sorting

class Weighted(models.Model):
	"Mix-in class. Manual sorting fields (coarse and fine, each [ 0..10, default 5 ])."
	sorting_weight = models.PositiveSmallIntegerField (
		choices = WEIGHTS_COARSE,
		default = DEFAULT_WEIGHT,
		help_text = "Coarse ordering control. 0 = first, 10 = last, 5 = default."
	)
	sorting_weight_fine_tune = models.PositiveSmallIntegerField (
		choices = WEIGHTS_FINE,
		default = DEFAULT_WEIGHT,
		help_text = "Fine ordering control, not usually needed. 0 = first, 10 = last, 5 = default."
	)


class Metadata(models.Model):
	"Mix-in class. CMS metadata, subset of Dublin Core standards."
	title = models.CharField ( max_length = 256, help_text = "Primary title.", )
	subtitle = models.CharField ( max_length = 256, help_text = "Secondary title.", )
	date = models.DateField (
		auto_now_add = True,
		help_text = "Publication date."
	)
	created = models.DateField( auto_now_add = True, )
	modified = models.DateField( auto_now = True, )
	description = models.CharField ( max_length = 256 )
	identifier = models.SlugField ( max_length = 128,
		unique = True,
		help_text = "A unique string (letters, numbers and underscores only) used in the URL.", 
	)
	language = models.CharField ( 
		max_length = 8,
		default = settings.DEFAULT_LANGUAGE,
		choices = settings.LANGUAGES,
		help_text = "The language this is written in.",
	)
	#contributors -> Author objects
	#creators -> Author object
	#subjects -> tagging
	
	## These fields skipped:
	#coverage
	#format
	#publisher
	#relation
	#rights
	#source
	#type

