"""
Django settings for twobuntu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os.path

ALLOWED_HOSTS = ['2buntu.com']
SITE_ID = 1

# Enable timezone-aware datetimes
USE_TZ = True
TIME_ZONE = 'America/Vancouver'

# Settings that control the delivery of email
EMAIL_BACKEND = 'pyhectane.django.HectaneBackend'
DEFAULT_FROM_EMAIL = SERVER_EMAIL = '2buntu <donotreply@2buntu.com>'

# Determine the directory this file resides in so that an absolute
# path can be specified for the static files and templates
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, 'static'),)
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, 'templates'),)

ROOT_URLCONF = 'twobuntu.urls'
WSGI_APPLICATION = 'twobuntu.wsgi.application'

INSTALLED_APPS = (
    # Core Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    # Django helper applications
    'django_archive',
    'widget_tweaks',
    # 2buntu applications
    'twobuntu.accounts',
    'twobuntu.api',
    'twobuntu.articles',
    'twobuntu.captcha',
    'twobuntu.categories',
    'twobuntu.images',
    'twobuntu.news',
    'twobuntu.shorturls',
    'twobuntu.touch',
)

MIDDLEWARE_CLASSES = (
    # Core Django middleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 2buntu middleware
    'twobuntu.middleware.ReadOnlyMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # Core Django context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # 2buntu context processors
    'twobuntu.context_processors.read_only',
)

# Router for database operations
DATABASE_ROUTERS = (
    'twobuntu.routers.ReadOnlyRouter',
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Load the debug toolbar if it is installed
try:
    import debug_toolbar
except ImportError:
    pass
else:
    INSTALLED_APPS = tuple(INSTALLED_APPS + ('debug_toolbar',))

# Import all local settings
from twobuntu.local_settings import *
