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



# Booleans
BOOLEANS = ((False,"No"),(True,"Yes"))


# Date-related constants
ONE_WEEK = datetime.timedelta(7)

##########
# 2-level Item Weighting
#
# Item weights from 0 through 10
MIN_WEIGHT = 0
DEFAULT_WEIGHT = 5
MAX_WEIGHT = 10

WEIGHTS_COARSE = WEIGHTS_FINE = [ [i,i] for i in range ( MIN_WEIGHT, MAX_WEIGHT + 1 ) ]
# customize some labels...
WEIGHTS_COARSE[MIN_WEIGHT][1] = "Lightest [%d]" % MIN_WEIGHT
WEIGHTS_COARSE[DEFAULT_WEIGHT][1] = "Default [%d]" % DEFAULT_WEIGHT
WEIGHTS_COARSE[MAX_WEIGHT][1] = "Heaviest [%d]" % MAX_WEIGHT

WEIGHTS_FINE[MIN_WEIGHT][1] = "Lighter [%d]" % MIN_WEIGHT
WEIGHTS_FINE[DEFAULT_WEIGHT][1] = "Default [%d]" % DEFAULT_WEIGHT
WEIGHTS_FINE[MAX_WEIGHT][1] = "Heavier [%d]" % MAX_WEIGHT

# Recursively tuple-ize the list of lists for performance
WEIGHTS_COARSE = tuple([ tuple(i) for i in WEIGHTS_COARSE ])
WEIGHTS_FINE = tuple([ tuple(i) for i in WEIGHTS_FINE ])

