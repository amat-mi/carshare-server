# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json
import os
import re
import sys

from django.core.management.base import NoArgsCommand, CommandError
from django.db import transaction
import requests

from carshare.models import Agency
from carshare.serializers import PinfVehicleSerializer, \
  PinfVehicleDataSerializer


def do_it():
  with requests.Session() as session:
    session.headers.update({'Authorization': 'Basic {}'.format(os.environ['DJANGO_CARSHARE_RETRIEVE_TOKEN'])})
    for agency in Agency.objects.all():
      try:        
        url = '{}?carAgency={}&type=car'.format(os.environ['DJANGO_CARSHARE_RETRIEVE_URL'],agency.id)
        content = session.get(url).text
        data = json.loads(content)
        for item in data['features']:        #per ogni dato di singolo veicolo nell'array 'features'
          vehicle_serializer = PinfVehicleSerializer.create_from_pinf(item)
          if vehicle_serializer.is_valid():
            vehicle_serializer.save()                                                
            data_serializer = PinfVehicleDataSerializer.create_from_pinf(item)
            if data_serializer.is_valid():
              data_serializer.save()                                                
            else:
              sys.stderr.write(data_serializer.errors)
          else:
            sys.stderr.write(vehicle_serializer.errors)
      except Exception, exc:
        sys.stderr.write(str(exc))
        raise exc
  
class Command(NoArgsCommand):
  help = u'Recupera la situazione attuale del CarSharing e la memorizza'
  
  def printline(self,msg):
    self.stdout.write(u'{}: {}\n'.format(msg,self.help))
    
  @transaction.atomic
  def handle_noargs(self, **options):
    self.printline('Inizio')
#     transaction.commit_unless_managed()
#     transaction.enter_transaction_management()
#     transaction.managed(True)
    try:
      do_it()
#       transaction.commit()
      self.printline('Fine')
    except Exception, exc:
#       transaction.rollback()
      raise CommandError(self.help + "\n" + str(exc))
#     finally:
#       transaction.leave_transaction_management()
