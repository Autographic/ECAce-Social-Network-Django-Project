from django.db import models
from photologue.models import Photo

class ProductColour(models.Model):
	name = models.CharField (
		max_length = 32,
		help_text = "A name for the colour.",
	)
	hexvalue = models.CharField (
		max_length = 6,
		help_text = "A CSS-style, 3-digit #rgb or 6-digit #rrggbb hexadecimal code, omitting the leading #.", 
	)
	def __unicode__(self): return "%s [#%s]" % ( self.name, self. hexvalue )

class Product(models.Model):
	name = models.CharField (
		max_length = 128,
		unique = True,
		help_text = "A product name, must be unique for each entry."
	)
	price = models.DecimalField ( decimal_places = 2, max_digits = 6, 
		help_text = "The retail price of this product, a.k.a. 'sticking it to the little guy.'",
	)
	cost = models.DecimalField ( decimal_places = 2, max_digits = 6, null=True, 
		help_text = "Optional. Our unit cost. Price minus cost equals PARTY MONEY!", 
	)
	teaser = models.CharField (
		max_length = 256,
		help_text = "A short, inviting blurb for listings pages.",
		blank = True, null = True,
	)
	about = models.TextField (
		help_text = "Unlimited length, basic HTML allowed. The full blurb for the product.",
		blank = True, null = True,
	)
	colours = models.ManyToManyField ( ProductColour,
		related_name = "products",
		help_text = "What colours are these products available in?",
	)
	# stock ->
	@property
	def same_colour_products(self):
		"Returns a dictionary of QuerySets, each containing the other Products in this colour."
		result = {}
		for c in self.colours.all():
			result[c.name] = c.products.exclude(self)
		return result
	
	def __unicode__(self):return self.name

class ProductPhoto(Photo):
	product = models.ForeignKey ( Product,
		related_name = "pictures",
	)
	def __unicode__(self): return u'Photo of %s' % self.product

class TeeShirtSize(models.Model):
	code = models.CharField (
		max_length = 4,
		help_text = "S,M,L,XL are common choices.",
	)
	label = models.CharField (
		max_length = 32,
		help_text = "'small', 'medium', you get it.",
	)
	def __unicode__(self): return self.label
	class Meta:
		verbose_name = "T-shirt size"

class TeeShirt(Product):
	sizes = models.ManyToManyField ( TeeShirtSize,
		help_text = "What sizes are these available in?",
	)
	def __unicode__(self): return self.name
	class Meta:
		verbose_name = "T-shirt"

class Inventory(models.Model):
	product = models.ForeignKey ( Product,
		related_name = "stock",
	)
	colour = models.ForeignKey ( ProductColour,
		related_name = "stocked_colours",
	)
	inventory = models.PositiveSmallIntegerField (
		help_text = "The number of these in stock.",
	)
	class Meta:
		verbose_name_plural = "inventory"

class TeeShirtInventory(Inventory):
	size = models.ForeignKey ( TeeShirtSize )
	class Meta:
		verbose_name_plural = "T-shirt inventory"

