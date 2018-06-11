# -*- coding: utf-8 -*-

# Add name and EMail address tuples
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Paolo', 'prove_django@oicom.com'),
)
MANAGERS = ADMINS

#PAOLO - Define a suitable value for From field (it will be used for exceptions EMails)
SERVER_EMAIL = 'AMAT carshare_server errors <info@amat-mi.it>'

# Set as needed
DATABASES = {
    'default': {
#           'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
          'ENGINE': 'django.contrib.gis.db.backends.postgis',
# PAOLO - In locale invece uso il nome che sarebbe giusto avere anche in remoto!!!           
          'NAME': 'django_amatdati',                      # Or path to database file if using sqlite3.
          'USER': 'django',                      # Not used with sqlite3.
          'PASSWORD': 'djangopass',                  # Not used with sqlite3.
          'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
          'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# List any hosts/domain names valid for this site (required if DEBUG is False)
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
#ALLOWED_HOSTS = []

# Make this unique, and don't share it with anybody.
SECRET_KEY = '01$k%#yn+rb_z_+o&!p3is4y$=r__hpdnk$0xmm1zl3b4lu8s_'

#####################################################
# Add here any additional or override settings needed
#####################################################
