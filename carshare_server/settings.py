# -*- coding: utf-8 -*-

from django.conf.global_settings import FORCE_SCRIPT_NAME
import os
import platform
#PAOLO - see: https://docs.djangoproject.com/en/1.4/topics/i18n/translation/#how-django-discovers-language-preference
ugettext = lambda s: s

RUNNING_MACHINE_NAME = platform.node().upper()

# By default this is NOT a DEV machine
IS_DEVELOPMENT_MACHINE = False  

# By default do NOT accept all origins for CORS
CORS_ORIGIN_ALLOW_ALL = False

# By default assets (ie: static, media, etc.) 
# are inside the project directories structure
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
# PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = PROJECT_PATH
MNT_PATH = PROJECT_PATH

# By default print EMails to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# By default no hosts/domain names are valid for this site (required if DEBUG is False)
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

#PAOLO - Ensure those cookies are only sent on secure (ie: https) connections for remote server
#There my be other things to do though, see:
#  http://security.stackexchange.com/questions/8964/trying-to-make-a-django-based-site-use-https-only-not-sure-if-its-secure
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Load mandatory local settings (may change any of the above settings)
try:
  from .local_settings_pre import *
except ImportError:
  raise Exception("Missing local_settings_pre.py file!!!")

DEBUG = IS_DEVELOPMENT_MACHINE #or RUNNING_MACHINE_NAME in ['WEB371.WEBFACTION.COM']
TEMPLATE_DEBUG = DEBUG

print(u'Project: "{}"'.format(PROJECT_PATH))
print(u'Running on: "{}"'.format(RUNNING_MACHINE_NAME))
print(u'With mnt: "{}"'.format(MNT_PATH))
print(u'Development machine: "{}"'.format('yes' if IS_DEVELOPMENT_MACHINE else 'no'))
print(u'Debug: "{}"'.format('yes' if DEBUG else 'no'))

#PAOLO - Send correct HTTP header for images 
#(see: http://stackoverflow.com/questions/16303098/django-development-server-and-mime-types)
#PAOLO - Send correct HTTP header for fonts (though fonts from Google Maps are wrong anyway...) 
#(see: #http://stackoverflow.com/questions/18271257/resource-interpreted-as-font-but-transferred-with-mime-type-font-woff-django)
if DEBUG:
  import mimetypes
  mimetypes.add_type("image/png", ".png", True)
  #mimetypes.add_type("application/font-woff", ".woff", True)
  mimetypes.add_type("application/x-woff", ".woff", True)
   
#PAOLO - following lines are to "mount" project under a subpath of the domain (ie: "example.com/project/")
#WARN!!! The same subpath must be correctly setup in configuring the HTTP front server!!!
if IS_DEVELOPMENT_MACHINE:
  FORCE_SCRIPT_NAME = ''
else:
  FORCE_SCRIPT_NAME = ''

# ATTENZIONE!!! Non funziona se FORCE_SCRIPT_NAME impostato a qualcosa!!!                     
LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME + '/'          #go to Home Page after Signin

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #PAOLO - Following is for GeoDjango
    'django.contrib.gis',             
     #PAOLO - Following is to use the Django REST Framework
    'rest_framework',       
   ############
    'carshare',
)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'carshare_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'carshare_server.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-it'

#PAOLO - Make only these languages available
LANGUAGES = (
    ('it', ugettext('Italian')),
)

#PAOLO - Change it from the default (0=Sunday)
FIRST_DAY_OF_WEEK = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

#PAOLO - Use the project locale directory too
LOCALE_PATHS = (
    os.path.abspath(os.path.join(PROJECT_PATH, 'locale')),
)

MEDIA_ROOT = os.path.join(MNT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#PAOLO - Usa i parametri corretti a seconda dell'host su cui sta girando
MEDIA_URL = '{}/media/'.format(FORCE_SCRIPT_NAME)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(MNT_PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
#PAOLO - Usa i parametri corretti a seconda dell'host su cui sta girando
STATIC_URL = '{}/static/'.format(FORCE_SCRIPT_NAME)

STATICFILES_DIRS = (
#     os.path.abspath(os.path.join(BASE_DIR, "../../static/")),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Load optional local settings
try:
  from .local_settings_post import *
except ImportError:
  pass 
