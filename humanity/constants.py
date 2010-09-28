MAX_NAME_LENGTH = 32 # Feel free to adjust this
PREFIX_LENGTH = 8 # Feel free to adjust this

NAME_FRAGMENT_TYPES = (
	('FAM','family'),
	('GIV','given'),
	('PRE','prefix'),
	('SUF','suffix'),
	('NICK','nickname'),
)

NAME_FRAGMENT_CODES = tuple( [i[0] for i in NAME_FRAGMENT_TYPES ] )

NAME_FRAGMENT_TYPES_HELP = {
	'FAM':  'You typically share your family name with brothers and sisters.',
	'GIV':  'Your family name is usually unique to you amongst your family members.',
	'PRE':  'A prefix appears before all other names, and is often an honorific such as Dr.',
	'SUF':  'Pertinent degrees and honorifics may be listed here.',
	'NICK': 'A chosen casual name, e.g. Skrud for Eitan "Skrud" Levi.',
}

NAME_STYLES = (
	('FORM', 'Formal full name and prefix/suffix'),
	('INF',  'Informal, given then family name'),
	('CAS',  'Casual, first name or nickname'),
	('SORT', 'Sorting: family name, comma, given name, middle name'),
)

# Item weights from 0 through 10
MIN_WEIGHT = 0
DEFAULT_WEIGHT = 5
MAX_WEIGHT = 10

WEIGHTS = [ [i,i] for i in range ( MIN_WEIGHT, MAX_WEIGHT + 1 ) ]
# customize some labels...
WEIGHTS[MIN_WEIGHT][1] = "Lightest [%d]" % MIN_WEIGHT
WEIGHTS[DEFAULT_WEIGHT][1] = "Default [%d]" % DEFAULT_WEIGHT
WEIGHTS[MAX_WEIGHT][1] = "Heaviest [%d]" % MAX_WEIGHT
# Tuple-ize it
WEIGHTS = tuple([ tuple(i) for i in WEIGHTS ])

# Can be made more GBLT-friendly as desired.
MALE = 'M'
FEMALE = 'F'
ITS_COMPLICATED = 'C'

GENDERS = (
	(MALE, 'male'),
	(FEMALE, 'female'),
	(ITS_COMPLICATED,"it's complicated"),
)


