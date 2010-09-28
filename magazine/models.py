from django.db import models
from django.conf import settings
from socialnetwork.base.models import Concordian, Weighted, Metadata
import tagging

class Author (SiteUser): 
	whoami = models.ForeignKey( HumanBeing
	# articles_contrib -> Article (as contributor)

class Department(models.Model):
	"An article category"
	name = models.CharField( max_length=32, )
	slug = models.SlugField( max_length=8, )

class Article (Metadata, Weighted):
	contributors = models.ManyToManyField ( Author,
		related_name = 'articles_contrib',
		blank = True,
	)
	primary_author = models.ForeignKey( Author,
		related_name = 'articles_primary',
		blank = True,
	)
	teaser = models.TextField (
		help_text = "A short introduction to entice the reader.",
	)
	department = models.ForeignKey ( Department,
		help_text = "What is the article category?",
	)
	bodytext_raw = models.TextField (
		help_text = "The original, unedited copy supplied.",
	)
	bodytext_cooked = models.TextField (
		help_text = "The edited final copy.",
		blank = True,
	)
	#title
	#subtitle
	#date
	#created
	#modified
	#description
	#identifier
	#language
	#creators -> Author object
	#subjects -> tagging

tagging.register(Article)
