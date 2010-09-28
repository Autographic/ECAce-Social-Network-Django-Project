from django import forms
#from constants import *
from models import *
from django.contrib import messages
from constants import *
import datetime

########## Fields ##########



########## Forms ##########

class HumanNameForm(forms.ModelForm):
	class Meta:
		model = HumanName

class HumanBeingForm(forms.ModelForm):
	class Meta:
		model = HumanBeing
	"""
	Form for registering a new user account.

	Validates that the requested username is not already in use, and
	requires the password to be entered twice to catch typos.

	Subclasses should feel free to add any additional validation they
	need, but should either preserve the base ``save()`` or implement
	a ``save()`` which accepts the ``profile_callback`` keyword
	argument and passes it through to
	``RegistrationProfile.objects.create_inactive_user()``.

	"""
	gender = forms.ChoiceField( choices = GENDERS, required=False, label=u'gender' )
	birthdate = forms.DateField( required=False, label=u'birthdate' )

	family_name = forms.CharField (
		help_text = 'Your family or "last" name.',
		label = 'family name',
	)
	given_name = forms.CharField (
		help_text = 'Your given or "first" name.',
		label = 'given name',
	)
	name_schema_family_last = forms.BooleanField ( initial = True,
		help_text = "If you write your family name after your own name, keep this checked.",
		label = 'name ordering',
	)

	def clean_gender(self):
		"""
		Validate that the gender is in the database.
		"""
		value = self.cleaned_data['gender']
		if not value: return None # not a required field
		try:
			return Gender.objects.get( label__iexact=value )
		except Gender.DoesNotExist:
		    raise forms.ValidationError(u'Invalid gender code "%s". If you take issue with this, please email marketing.director@ecaconcordia.ca for assistance.' % value )
		
	def clean_birthdate(self):
		"""
		Ensure an age from 15 to 100 for university students.
		"""
		value = self.cleaned_data['birthdate']
		if not value: return None # not a required field
		max_value = datetime.date.today() - datetime.timedelta( int(25*365.24) ) # Surely everyone's at least 15.
		min_value = datetime.date.today() - datetime.timedelta( 36524 ) # Centenarians are welcome, however, should they wish to attend.
		if value < min_value or value > max_value:
		    raise forms.ValidationError(u'Invalid age (%s). If you take issue with this, please email marketing.director@ecaconcordia.ca for assistance.' % value )
		return value

	def clean_family_name(self):
		"""
		Just stripping whitespace and ensuring some value.
		"""
		value = self.cleaned_data['family_name'].strip()
		if not value:
		    raise forms.ValidationError(u'No family name was supplied.' )
		return value

	def clean_given_name(self):
		"""
		Just stripping whitespace and ensuring some value.
		"""
		value = self.cleaned_data['given_name'].strip()
		if not value:
		    raise forms.ValidationError(u'No given name was supplied.' )
		return value
	'''
	def clean(self):
		"""
		Verifiy that the values entered into the two password fields
		match. Note that an error here will end up in
		``non_field_errors()`` because it doesn't apply to a single
		field.
		
		"""
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
		    if self.cleaned_data['password1'] != self.cleaned_data['password2']:
		        raise forms.ValidationError(_(u'You must type the same password each time'))
		return self.cleaned_data
	'''
	def save(self, profile_callback=None):
		"""
		Create the new ``HumanName``, returns the ``HumanBeing``.
		
		This is essentially a light wrapper around
		``RegistrationProfile.objects.create_inactive_user()``,
		feeding it the form data and a profile callback (see the
		documentation on ``create_inactive_user()`` for details) if
		supplied.
		
		"""
		human = HumanBeing.people.create(
			gender = self.gender,
			birthdate = self.birthdate,
		)
		human.name.create (
			given_name = self.given_name,
			family_name = self.family_name,
			name_schema_family_last = self.name_schema_family_last,
		)
		return human


