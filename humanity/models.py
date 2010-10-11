from django.db import models
from constants import *

def create_human(family_name, given_name='' ):
	human = HumanBeing.objects.create()
	
	
class Gender(models.Model):
	abbrev = models.CharField (
		max_length=2, 
		unique = True,
		primary_key=True,
		help_text = 'A unique, single character abbreviation, e.g., "f" for female.',
	)
	label = models.CharField (
		max_length=32, 
		unique = True,
		help_text = "There are two of these, or more depending on your viewpoint.",
	)
	def _ensure_minimum_data (self):
		"Initialize instances with human sexes, if no instances already exist."
		qs = self.__class__.objects
		if not qs.count():
			qs.create( abbrev = FEMALE, label = 'female' )
			qs.create( abbrev = MALE, label = 'male' )
	
	@property
	def is_male(self):
		return self.abbrev.lower() =='m'
	@property
	def is_female(self):
		return self.abbrev.lower() =='f'
	@property
	def is_complicated(self):
		return self.abbrev.lower() =='c'

	@classmethod
	def get_male(cls):
		return cls.objects.get( abbrev__lower ='m' )
	@classmethod
	def get_female(cls):
		return cls.objects.get( abbrev__lower ='f' )
	@classmethod
	def get_complicated(cls):
		return cls.objects.get( abbrev__lower ='c' )
	@classmethod
	def get_for(cls,value):
		v = value[0].lower()
		return cls.objects.get( abbrev__lower = v )
	
	def __unicode__(self): return self.label

class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter( gender = MALE )

class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter( gender = FEMALE )


class HumanBeing(models.Model):
	"A creature of subspecies Homo sapiens sapiens."
	# name -> HumanName instance for flexibility
	gender = models.ForeignKey ( Gender,
		null = True, blank = True,
		help_text = "Optional. Your gender.",
	)
	birthdate = models.DateField (
		blank = True, null=True,
		help_text = "Optional, but filling this in can result in a lot of happy birthday messages!",
	)
	class Meta:
		verbose_name_plural = "people"
	@property
	def gender_possessive(self,language='en'):
		s = "their"
		if self.gender.is_male: s = "his"
		if self.gender.is_female: s = "her"
		return s
	
	@property
	def gender_pronoun(self,language='en'):
		s = "they"
		if self.gender.is_male: return u"he"
		if self.gender.is_female: return u"she"
		return s

	men = MaleManager()
	women = FemaleManager()
	people = models.Manager()
	objects = models.Manager() # It's nothing personal, really. Just for coding convenience. :-)
	
	def __unicode__(self):
		try:
			return unicode(self.name)
		except AttributeError: return 'Anonymous'
	
	@property
	def sorting_name(self):
		return self.name.sorting
	@property
	def full_name(self):
		return self.name.full
	@property
	def given_name(self):
		return self.name.given
	@property
	def family_name(self):
		return self.name.family
		

class HumanName(models.Model):
	"A human has formal, informal, and casual names: more than one, in short."
	whoami = models.OneToOneField ( HumanBeing,
		related_name = 'name',
		help_text = "Whose name is this?",
		unique = True,
	)
	given = models.CharField (
		max_length = 32,
		help_text = "Your given name.",
	)
	middle = models.CharField (
		max_length = 32,
		help_text = "Optional. Middle name or initial.",
		blank = True,
	)
	family = models.CharField (
		max_length = 32,
		help_text = "Your family name.",
	)
	
	prefix = models.CharField (
		max_length = 32,
		help_text = "Optional. Stuff before all other name parts: Dr, Mr, Ms/Mrs/Miss, etc.",
		blank = True,
	)
	suffix = models.CharField (
		max_length = 32,
		help_text = "Stuff after all other name parts, such as degrees or Orders of the British Empire.",
		blank = True,
	)
	
	name_schema_family_last = models.BooleanField(
		default = True,
		help_text = "Does your family name appear before your given name in your complete neme? Deselect this.",
	)
	
	def __unicode__(self): return self.sorting
	
	@property
	def formal(self):
		# gather the (potential) pieces
		if self.name_schema_family_last:
			parts = [ self.prefix, self.given, self.middle, self.family, self.suffix, ]
		else:
			parts = [ self.prefix, self.family, self.given, self.middle, self.suffix, ]
		# filter empty parts
		parts = [ pt for pt in parts if len(pt) ]
		# join them into a Unicode string
		return u' '.join( parts )
		
		# Note: this can be written in one line:
		#return u' '.join( [ pt for pt in ( self.first, self.middle, self.last ) if len(pt) ] )

	@property
	def full(self):
		# gather the (potential) pieces
		if self.name_schema_family_last:
			parts = [ self.given, self.middle, self.family, ]
		else:
			parts = [ self.family, self.middle, self.middle, ]
		# filter empty parts
		parts = [ pt for pt in parts if len(pt) ]
		# join them into a Unicode string
		return u' '.join( parts )
		
		# Note: this can be written in one line:
		#return u' '.join( [ pt for pt in ( self.first, self.middle, self.last ) if len(pt) ] )
	
	@property
	def informal(self):
		# gather the (potential) pieces
		if self.name_schema_family_last:
			parts = [ self.given, self.family, ]
		else:
			parts = [ self.family, self.given, ]
		# filter empty parts
		parts = [ pt for pt in parts if len(pt) ]
		# join them into a Unicode string
		return u' '.join( parts )
	
	@property
	def sorting(self):
		# gather the (potential) pieces
		parts = [ self.family, self.given, ]
		# filter empty parts
		parts = [ pt for pt in parts if len(pt) ]
		# join them into a Unicode string
		return u', '.join( parts )
	
	@property
	def casual(self): return self.given

