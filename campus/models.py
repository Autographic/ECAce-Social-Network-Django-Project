from django.db import models

CAMPUSES = (
	('SGW','Sir George Williams'),
	('LOY','Loyola'),
)

class Campus(models.Model):
	code = models.CharField (
		primary_key = True,
		max_length = 3,
		choices = CAMPUSES,
		help_text = "Sir George Williams (Downtown) or Loyola?",
	)
	name = models.CharField (
		max_length = 64,
		help_text = "The proper name of the campus.",
		
	)
	notes = models.TextField (
		help_text = "Any comments on this campus, e.g. how to find Loyola.",
		blank = True,
	)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = 'campuses'


class Building(models.Model):
	campus = models.ForeignKey ( Campus,
		related_name = 'buildings',
	)
	name = models.CharField (
		max_length = 64,
		help_text = "The proper name of the campus.",
		
	)
	code = models.CharField (
		max_length = 3,
		help_text = "The letter designating the building, i.e. H for the Hall Building.",
		
	)
	notes = models.TextField (
		help_text = "Any comments on this building, e.g. how to find CB.",
		blank = True,
	)
	
	# classrooms -> Classroom
	def __unicode__(self):
		return u'%s building [%s]' % ( self.code, self.campus )

class Classroom(models.Model):
	building = models.ForeignKey ( Building,
		related_name = "classrooms",
		help_text = "The building containing this classroom.",
	)
	number = models.CharField (
		max_length = 8,
		help_text = "The room number; e.g. 407 for SGW H-407.",
	)
	notes = models.TextField (
		help_text = "Any comments on this room.",
		blank = True,
	)
	
	def __unicode__(self):
		return u'[%s] %s-%s' % ( self.building.campus, self.building.code, self.number, )


