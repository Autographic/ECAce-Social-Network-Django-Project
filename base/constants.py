
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

