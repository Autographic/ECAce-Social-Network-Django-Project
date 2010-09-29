""" Settings for Autographic social network system
By MJP Sep 4 2010. New start using model inheritance.
"""

import os, django

# Record Django's root in the filesystem
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
# Record this project's root in the filesystem
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# Record this project's name
PROJECT_NAME = PROJECT_ROOT.replace('/','')

# Determine if this is the development or deployment version
# (Development version is placed in the filesystem root in the socialnetwork directory)
IS_DEV_SERVER = PROJECT_ROOT == '/socialnetwork'

# Continue with standard Django settings...
DEBUG = IS_DEV_SERVER # True
TEMPLATE_DEBUG = DEBUG

gettext_noop = lambda s: s

ADMINS = (
    ('Murray Pearson','murray@autographic.ca'),
    ('Sandy Woo','marketing@ecaconcordia.ca'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Canada/Montreal'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-CA'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
if IS_DEV_SERVER:
	MEDIA_URL = 'http://ecace/media_socialnetwork/base/'
else:
	MEDIA_URL = 'http://media.ecace.autographic.ca/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v-*=tgb2l#%9bkf_1ix0m=g5*wdyf6tk+t+22s%n13nnuq5nhp'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

APPEND_SLASH = True
PREPEND_WWW = False

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates/' % PROJECT_ROOT
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.contrib.messages.context_processors.messages",
	#"socialnetwork.context_processors.load_settings", # doesn't exist just yet
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'photologue','tagging',
    'registration','profiles', # Django extensions

    '%s.base' % PROJECT_NAME, # Site configuration
    '%s.humanity' % PROJECT_NAME, # HumanBeing, HumanName
    '%s.concordia' % PROJECT_NAME, # Concordian, Student, Professor, TA
    '%s.attachment' % PROJECT_NAME, # File attachment infrastructure
    #'%s.magazine' % PROJECT_NAME, # CMS
    #'%s.forum' % PROJECT_NAME, # Threaded discussions
    #'%s.blog' % PROJECT_NAME, # Why not?
)

FIXTURES_DIRECTORIES = (
	'%s/fixtures/' % PROJECT_ROOT,
)

# Date formatting
DATETIME_FORMAT = 'N j, Y'
MONTH_DAY_FORMAT = 'N j'
TIME_FORMAT = 'p'
YEAR_MONTH_FORMAT = 'F Y'

# i18n
LANGUAGES = (
    ('en', gettext_noop('English')),
    ('fr', gettext_noop('French')),
)
DEFAULT_LANGUAGE = 'en'

# Server mail
# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = 'murray@autographic.ca' # TODO: create webserver address @ecaconcordia.ca
EMAIL_SUBJECT_PREFIX = '[ECAce] '

# Registration settings
ACCOUNT_ACTIVATION_DAYS = 7 # Give 'em a week

# The profile automatically created for each Student
AUTH_PROFILE_MODULE = 'concordia.Concordian'
LOGIN_REDIRECT_URL = '/'


