from django.test import TestCase
from models import *

from cStringIO import StringIO

TITLE_TEMPLATE = 'test file %d'
FILENAME_TEMPLATE = "%s.txt" % ( TITLE_TEMPLATE.replace(' ','_'), )

MAX_FILES = 8
def get_title():
	"A numerical title generator"
	for i in range(MAX_FILES):
		yield TITLE_TEMPLATE % i
def get_filename():
	"A numerical filename generator"
	for i in range(MAX_FILES):
		yield FILENAME_TEMPLATE % i

TEXT_TEXT = """This is the test file.
It contains several lines and some blank lines.

Here is the last line of the initial entry."""

APPENDAGE = """This text is appended onto the first test.

This is the end of the appendage.
"""


class AttachmentTest(TestCase):
	def setUp(self):
		"Prepare simulated attachement file-like object"
		self.attachment = StringIO()
		print >> self.attachment, TEST_TEXT
	
	def test_upload(self):
		"'Upload' a file-like object"
		pass
		f = self.attachment
		# test object creation
		# test upload process
		att = Attachment.objects.create(
			title=get_title(),
			filename=get_filename(),
			attachment = self.attachment,
		)
		
		# test versioning
		self.failUnlessEqual(att.versions, 1)
		
		print >> self.attchment, APPENDAGE
		att.upload_new_version( self.attchment )
		
		self.failUnlessEqual(att.versions, 2)

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

