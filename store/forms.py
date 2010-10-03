from django import forms
from models import *

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
	name = forms.CharField (
		help_text = "A product name, must be unique for each entry."
	)
	price = forms.DecimalField ( places = 2, max_places = 6, 
		help_text = "The price, in Simoleons or something.",
	)
	cost = forms.DecimalField ( places = 2, max_places = 6, blank=True,
		help_text = "Optional. The item cost to the ECA.",
	)

class ProductPhotoForm(forms.ModelForm):
	product = forms.ForeignKeyField ( Product,
		related_name = "pictures",
	)
	class Meta:
		model = ProductPhoto

class TeeShirtSizeForm(forms.ModelForm):
	class Meta:
		model = TeeShirtSize

class TeeShirtForm(forms.ModelForm):
	class Meta:
		model = TeeShirt

