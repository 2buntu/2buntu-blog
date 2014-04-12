'''
Django settings for twobuntu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
'''

import os.path

ALLOWED_HOSTS = ['2buntu.com',]
SITE_ID       = 1

# Enable timezone-aware datetimes
USE_TZ    = True
TIME_ZONE = 'America/Vancouver'

# Determine the directory this file resides in so that an absolute
# path can be specified for the static files and templates
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
TEMPLATE_DIRS    = (os.path.join(PROJECT_ROOT, 'templates'),)

ROOT_URLCONF     = 'twobuntu.urls'
WSGI_APPLICATION = 'twobuntu.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
)

INSTALLED_APPS = (
    # Core Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django helper applications
    'south',
    'widget_tweaks',
    # 2buntu applications
    'twobuntu.accounts',
    'twobuntu.ads',
    'twobuntu.api',
    'twobuntu.articles',
    'twobuntu.categories',
    'twobuntu.images',
    'twobuntu.news',
)

# Load the debug toolbar if it is installed
try:
    import debug_toolbar
except ImportError:
    pass
else:
    INSTALLED_APPS = tuple(INSTALLED_APPS + ('debug_toolbar',))

# Import all local settings
from local_settings import *
