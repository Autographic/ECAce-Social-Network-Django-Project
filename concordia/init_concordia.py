# This should be replaced by a database fixture: MJP Sep 27/10

from models import Discipline
from constants import *

for p in ENCS_PROGRAMS:
	try:
		o = Discipline.objects.get(code = p[0] )
		o.name = p[1]
		o.save()
	except Discipline.DoesNotExist:
		Discipline.objects.create(code=p[0],name=p[1])

