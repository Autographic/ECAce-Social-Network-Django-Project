from django.db import models
from django.contrib.humanize.templatetags import ordinal
import datetime, random

class Competition(models.Model):
	name = models.CharField (
		max_length = 128,
		help_text = "The competition's full, official name, e.g., Troitsky Bridge Building Competition.",
	)
	nickname = models.CharField (
		max_length = 32,
		help_text = "The short-hand name, e.g., Troitsky.",
	)
	founding_year = models.PositiveSmallIntegerField (
		help_text = "What year was the competition founded? This is used to calculate annual event numbers.",
	)
	slogan = models.CharField (
		max_length = 256,
		blank=True,
		help_text = "Optional. The competition slogan.",
	)
	about = models.TextField (
		blank = True, null = True,
		help_text = "Optional. A teaser blurb about the competiton for the listings page.",
	)

class Event(models.Model):
	"An annual instance of the competition."
	competition = models.ForeignKey ( Competition, )
	year = models.PositiveSmallIntegerField (
		default = datetime.date.today().year, # Let's hope this works ;-)
		help_text = "The nominal year of the competition, used to generate the ordinal value.",
	)
	@property
	def ordinal_year(self):
		return 1 + self.year - self.competition.founding_year,
	@property
	def get_ordinal_year_display(self):
		return ordinal(self.ordinal_year)
	
	annual_slogan =  = models.CharField (
		max_length = 256,
		blank=True,
		help_text = "Optional. The competition slogan FOR THIS YEAR.",
	)
	@property
	def slogan(self):
		return self.annual_slogan or self.competition.slogan
	
