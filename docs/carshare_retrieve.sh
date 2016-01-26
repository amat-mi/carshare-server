#!/bin/bash

echo "
##########################################################################
"
date

export DJANGO_CARSHARE_RETRIEVE_TOKEN="xxxxxxxxxxxxxxxxxxxxxx"
export DJANGO_CARSHARE_RETRIEVE_URL="xxxxxxxxxxxxxxxxxxxxxx"

/var/www/django/django-manage.sh carshare-server carshare_retrieve

date
