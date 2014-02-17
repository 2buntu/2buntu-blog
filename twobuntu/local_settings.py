'''
Installation-specific settings for 2buntu

Anything that is specific to your installation of 2buntu should
be included here and NOT in settings.py
'''

# Set DEBUG to True to enable full debugging in your application
DEBUG          = False
TEMPLATE_DEBUG = DEBUG

# Database storage engine(s) for the project
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     '',
        'USER':     '',
        'PASSWORD': '',
        'HOST':     '',
        'PORT':     '',
    },
}

# Absolute filesystem path where media (uploaded) and static files will be stored
MEDIA_ROOT  = ''
STATIC_ROOT = ''

# URL for media and static files
MEDIA_URL  = '/media/'
STATIC_URL = '/static/'

# This value must be customized
SECRET_KEY = ''
