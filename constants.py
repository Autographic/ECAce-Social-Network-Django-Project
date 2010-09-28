"""constants.py
Constants used in the ECA sites.
Created Aug 1 2010 by MJP
"""

import datetime

THIS_YEAR = 2010 # Update as needed, or automate this value

# Popup choice lists
JAN = JANUARY = "01"
FEB = FEBRUARY = "02"
MAR = MARCH = "03"
APR = APRIL = "04"
MAY = "05"
JUN = JUNE = "06"
JUL = JULY = "07"
AUG = AUGUST = "08"
SEP = SEPTEMBER = "09"
OCT = OCTOBER = "10"
NOV = NOVEMBER = "11"
DEC = DECEMBER = "12"

MONTHS = (
	( JAN, 'January'),
	( FEB, 'February'),
	( MAR, 'March'),
	( APR, 'April'),
	( MAY, 'May'),
	( JUN, 'June'),
	( JUL, 'July'),
	( AUG, 'August'),
	( SEP, 'September'),
	( OCT, 'October'),
	( NOV, 'November'),
	( DEC, 'December'),
)

WEEKDAYS = (
	(1,"Monday"),
	(2,"Tuesday"),
	(3,"Wednesday"),
	(4,"Thursday"),
	(5,"Friday"),
	(6,"Saturday"),
	(7,"Sunday"),
)

def weekday_code(name):
	for day in DAYS_OF_WEEK:
		if name.lower()==day[1].lower():return day[0]

WEEKS = ((0,'Every Week'),(1,'Week One'),(2,'Week Two'))

SEMESTERS = ((1,'Summer'),(2,'Fall'),(3,'Fall/Winter'),(4,'Winter'),)
def semester_code(name):
	for semester in SEMESTERS:
		if name.lower()==semester[1].lower():return semester[0]

CAMPUSES = (('SGW','Sir George Williams (Downtown)'),('LOY','Loyola Campus'))


# ENCS Programs

BLDG_ENG_NAME     = "Building Engineering"
CIV_ENG_NAME      = "Civil Engineering"
COMP_ENG_NAME     = "Computer Engineering"
ELEC_ENG_NAME     = "Electrical Engineering"
IND_ENG_NAME      = "Industrial Engineering"
MECH_ENG_NAME     = "Mechanical Engineering"
SOFT_ENG_NAME     = "Software Engineering"
COMP_SCI_NAME     = "Computer Science"
COMP_SCI_MIN_NAME = "Computer Science (minor)"

BLDG_ENG     = "BLDG"
CIV_ENG      = "CIVI"
COMP_ENG     = "COMP"
ELEC_ENG     = "ELEC"
IND_ENG      = "IND"
MECH_ENG     = "MECH"
SOFT_ENG     = "SOFT"
COMP_SCI     = "CSCI"
COMP_SCI_MIN = "CSCm"

ENCS_PROGRAMS = (
	( BLDG_ENG,  BLDG_ENG_NAME ),
	( CIV_ENG,  CIV_ENG_NAME ),
	( COMP_ENG,  COMP_ENG_NAME ),
	( ELEC_ENG,  ELEC_ENG_NAME ),
	( IND_ENG,   IND_ENG_NAME ),
	( MECH_ENG,  MECH_ENG_NAME ),
	( COMP_SCI,  COMP_SCI_NAME ),
	( COMP_SCI_MIN, COMP_SCI_MIN_NAME ),
)

ENCS_DEPARTMENTS = {
	'MIE':(MECH_ENG, IND_ENG,),
	'BCE':(BLDG_ENG,CIV_ENG,),
	'ECE':(ELEC_ENG,COMP_ENG,),
	'CSE':(SOFT_ENG,COMP_SCI,COMP_SCI_MIN,),
}

PROGRAM_YEARS = (
	( 1, 'Froshie' ),
	( 2, 'Second year' ),
	( 3, 'Third year' ),
	( 4, 'Fourth year' ),
	( 5, 'Fifth(?) year' ),
	( 6, 'Professional student' ),
	( 7, 'Seriously considering graduation' ),
	( 8, 'Seriously considering retirement' ),
)


# Booleans
BOOLEANS = ((False,"No"),(True,"Yes"))

# Item weights from 0 through 10
MIN_WEIGHT = 0
DEFAULT_WEIGHT = 5
MAX_WEIGHT = 10

WEIGHTS = [ [i,i] for i in range ( MIN_WEIGHT, MAX_WEIGHT + 1 ) ]
# customize some labels...
WEIGHTS[MIN_WEIGHT][1] = "Weightless [%d]" % MIN_WEIGHT
WEIGHTS[DEFAULT_WEIGHT][1] = "Default [%d]" % DEFAULT_WEIGHT
WEIGHTS[MAX_WEIGHT][1] = "Neutronium [%d]" % MAX_WEIGHT
# Tuple-ize it
WEIGHTS = tuple([ tuple(i) for i in WEIGHTS ])



# Date-related constants
ONE_WEEK = datetime.timedelta(7)
APP_START_DATE = datetime.date( 2010, 8, 8 ) # Sun Sep 8


# Status codes
STATUS_PENDING = 'pending'
STATUS_CURRENT = 'current'
STATUS_EXPIRED = 'expired'
STATUS_UNAPPROVED = 'unapproved'

def display_status(obj, approved, start, stop):
	"Returns the status code for the object."
	if not approved: return STATUS_UNAPPROVED
	today = datetime.date.today()
	if today > stop: return STATUS_EXPIRED
	if today < start: return STATUS_PENDING
	return STATUS_CURRENT

