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


SEMESTERS = (
	(1,'Spring/Summer'),
	(2,'Fall'),
	(3,'Fall/Winter'),
	(4,'Winter'),
)
