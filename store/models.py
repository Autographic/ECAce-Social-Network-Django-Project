from django.db import models
from photologue.models import PictureModel

class Product(models.Model):
	name = models.CharField (
		unique = True,
		help_text = "A product name, must be unique for each entry."
	)
	price = models.DecimalField ( places = 2, max_places = 6, )
	cost = models.DecimalField ( places = 2, max_places = 6, null=True, )

class ProductPhoto(PictureModel):
	product = models.ForeignKey ( Product,
		related_name = "pictures",
	)

class TeeShirtSize(models.Model):
	code = models.CharField (
		max_length = 4,
		help_text = "S,M,L,XL are common choices.",
	)
	label = models.CharField (
		max_length = 32,
		help_text = "'small', 'medium', you get it.",
	)

class TeeShirt(models.Model):
	product = models.ForeignKey ( Product, related_name="t_shirts" )
	sizes = models.ManyToManyField ( TeeShirtSize,
		help_text = "What sizes are these available in?",
	)
