from django import forms
#from constants import *
from models import *
from django.contrib import messages

from registration.forms import RegistrationForm

########## Fields ##########



########## Forms ##########

class DisciplineForm(forms.ModelForm):
	class Meta:
		model = Discipline
class AvatarForm(forms.ModelForm):
	class Meta:
		model = Avatar
class ConcordianRegistrationForm(RegistrationForm):
	class Meta:
		model = Concordian
class StudentForm(forms.ModelForm):
	class Meta:
		model = Student

class StudentIDForm(forms.Form):
	student_id = forms.RegexField( r'^\d{7}$',
		help_text = "Your 7-digit Concordia student ID number.",
	)
	family_name = forms.CharField ( 
		max_length = 32,
		help_text = "Enter your family name ('last name') here to confirm your ID.",
	)
	def clean_student_id(self):
		value = self.cleaned_data['student_id']
		try:
			assert(len(str(value))==7)
			value = u'%07d' % int(value)
		except:
			raise forms.ValidationError(u'Invalid student ID "%s".' % value )
		try:
			self.user = User.objects.get(username = value) # We must PREMAKE student users! Good security start.
		except User.DoesNotExist:
			raise forms.ValidationError(u'Unknown student ID "%s". Please visit the ECA office in H-838 to obtain an account.' % value)
		return value

class ProfessorForm(forms.ModelForm):
	class Meta:
		model = Professor

class TeachingAssistantForm(forms.ModelForm):
	class Meta:
		model = TeachingAssistant

