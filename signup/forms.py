from django import forms
#from constants import *
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm

from socialnetwork.academics.models import *
from socialnetwork.humanity.models import *

########## Fields ##########



########## Forms ##########

class ECAceRegControllerForm(forms.Form):
	family_name = forms.CharField (
		max_length=64,
	)
	student_id = forms.RegexField ( r'^\d{7}$',
	)
	def clean(self):
		self.cleaned_data['hexdigest'] = ECAceRegistrationControl.hash_value( 				
			student_id = self.cleaned_data['student_id'],			
			family_name = self.cleaned_data['family_name'].upper()
		)
		
	
	def find(self):
		if not self.hexdigest: self.clean()
		
	
class ConcordianRegistrationForm(forms.ModelForm):
	class Meta:
		model = Concordian


class StudentIDForm(forms.Form):
	student_id = forms.RegexField( r'^\d{7}$',
		help_text = "Required. Your 7-digit Concordia student ID number. This will be securely kept.",
		label = 'Student ID'

	)
	family_name = forms.CharField ( 
		max_length = 32,
		help_text = "Enter your family name ('last name') here to confirm your ID.",
	)
	def clean_student_id(self):
		value = self.cleaned_data['student_id']
		# Paranoiacally validate
		try:
			# the value must be seven digits long
			assert(len(str(value))==7)
			# the value must coerce to an integer
			value = u'%07d' % int(value)
		except:
			raise forms.ValidationError(u'Invalid student ID "%s".' % value )
		return value

	def clean_family_name(self):
		value = self.cleaned_data['family_name'].strip()
		return value

	def clean(self):
		sid = self.cleaned_data.get('student_id')
		name = self.cleaned_data.get('family_name')
		RC = ECAceRegistrationControl
		try:
			self.user_ticket = RC.objects.get(hexdigest=RC.hash_values(sid,name))
		except RC.DoesNotExist:
			raise forms.ValidationError(u"Sorry, the student ID and name don't match our records. See the ECA office, H-838, for assistance.")
		return self.cleaned_data
	
	def save(self):
		self.user_ticket.delete()
		return self.cleaned_data




