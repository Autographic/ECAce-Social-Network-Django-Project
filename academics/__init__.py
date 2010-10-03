import datetime

def get_current_school_year():
	"Utility method: returns the current *academic* year."
	today = datetime.date.today()
	year = today.year
	# School year starts in late August, more or less
	if today.month < 8 or today.month == 8 and today.day < 20:
		year -= 1
	return year

