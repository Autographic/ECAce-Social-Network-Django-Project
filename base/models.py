from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from socialnetwork.humanity.models import HumanBeing
from constants import *
from django.conf import settings
import hashlib

"""	Social Network Base Classes
SocialNetworkSite
Weighted, Metadata
"""

#########
# Created Sep 4 2010 by MJP
#

class SocialNetworkSite (Site):
	"Custom sitewide settings, mostly for templating customization"
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


class Weight(models.Model):
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
	class Meta:
		verbose_name = "weighting"


class Metadata(models.Model):
	"Mix-in class. CMS metadata, subset of Dublin Core standards."
	title = models.CharField ( max_length = 256, help_text = "Primary title.", )
	subtitle = models.CharField ( max_length = 256, help_text = "Secondary title.", )
	date = models.DateField (
		auto_now_add = True,
		help_text = "Publication date."
	)
	status = models.CharField ( 
		max_length=1,
		choices = STATUS_CODES,
	)
	publish_starting = models.DateField( auto_now_add = True, )
	expiry_date = models.DateField( auto_now_add = True, )
	approved_by_user = models.ForeignKey( User, related_name = 'approved_items' )
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
	class Meta:
		verbose_name_plural = "metadata"
	def update_status(self, start_date, stop_date):
		"Returns the status code for the object in the date range given."
		if not approved: return STATUS_UNAPPROVED
		today = datetime.date.today()
		if today > stop_date: return STATUS_EXPIRED
		if today < start_date: return STATUS_PENDING


class RegistrationLimiter(models.Model):
	"A generic hashed-value storage system. Subclass and implement the hash_values class method as needed."
	hexdigest = models.CharField (
		max_length = 64,
		help_text = "The encrypted value.",
		unique = True,
	)
	def __unicode__ (self):
		"Returns only a partial chunk of the hash, uniqueness not guaranteed!"
		clip = self.hexdigest[:12]
		return u'[ %s... ]' % clip
	crypto_method = hashlib.sha256

	salt = None		# This should be a short random string in subclasses
	case_sensitive = False
	strip_whitespace = True
	force_ascii = True
	@classmethod
	def hash_values(cls, *values):
		if cls.force_ascii: values = [ '%s'%i for i in values ] # convert values to ASCII
		if cls.strip_whitespace: values = [ s.strip() for s in values ] # strip whitespace
		if not cls.case_sensitive: values = [ s.upper() for s in values ] # case insensitivity
		return self.crypto_method( self.salt.join(values) ).hexdigest()

