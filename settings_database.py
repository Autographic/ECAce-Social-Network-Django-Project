# On deployment servers, compile this into .pyc bytecode and then delete this file from the server.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_ecace',                      # Or path to database file if using sqlite3.
        'USER': 'Django',                      # Not used with sqlite3.
        'PASSWORD': 'SECRET',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
}

