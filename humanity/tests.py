from models import HumanBeing, HumanName, NameFragment
from constants import *
from django.test import TestCase
import datetime

NAME_DATA = (
	('Alice', { # name
		'given':  'Alice', 
		'family': 'Hypothetical',
	},{ # personal
		'gender': FEMALE,
		'birthdate': datetime.date(1980, 1, 2),
	}),
	('Bob', { # name
		'given':  'Bob', 
		'family': 'Scott',
		'nickname': 'Bobo',
	},{ # personal
		'gender': MALE,
		'birthdate': datetime.date(1960, 8, 18),
	}),
)
class HumanTest(TestCase):
	def setUp(self):
		for entry in NAME_DATA:
			name = HumanName.objects.create(**entry[1])
			person = HumanBeing.objects.create(**entry[2])
	def TestNames(self):
		people = HumanBeing.objects.order_by('id')
		compare = zip(people, NAME_DATA)
		for who, what in compare:
			key, name, personal = what
			self.FailUnlessEqual(who.name.given, name['given'])
			self.FailUnlessEqual(who.name.family, name['family'])
			

