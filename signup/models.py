from django.db import models
from django.contrib.auth.models import User
from photologue.models import ImageModel
import datetime, random, hashlib

from socialnetwork.base.models import RegistrationLimiter
from socialnetwork.humanity.models import HumanBeing

from constants import *
#from utils import *

######### Registration Control
class ECAceRegistrationControl (RegistrationLimiter):
	"Registration is limited to enrolled students by their ID number and family name."
	# hexdigest 64-character field is inherited
	salt = 'gxbhy+' # ECA
	crypto_method = hashlib.sha256
	@classmethod
	def hash_values(cls, student_id, family_name):
		# This should vary randomly from class to class, if this code is reused
		glommed = cls.salt.join([ "%s"%i for i in [ student_id, family_name ] ])
		return cls.crypto_method( glommed ).hexdigest()
	class Meta:
		verbose_name = "ECAce registration control"



