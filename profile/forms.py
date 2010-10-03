from django import forms
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm

from models import *
from socialnetwork.humanity.models import *
########## Forms ##########

class AvatarForm(forms.ModelForm):
	class Meta:
		model = Avatar

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student

class ProfessorForm(forms.ModelForm):
	class Meta:
		model = Professor

class TeachingAssistantForm(forms.ModelForm):
	class Meta:
		model = TeachingAssistant

