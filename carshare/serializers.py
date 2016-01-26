# coding: utf-8

from datetime import datetime

from django.contrib.gis.geos.geometry import GEOSGeometry
import pytz
from rest_framework import serializers

from models import Vehicle, VehicleStatus, VehicleData


#################################################
class VehicleStatusSerializer(serializers.ModelSerializer):
  pass

  class Meta:
    model = VehicleStatus
    exclude = ['id','vehicle']

#################################################
class VehicleSerializer(serializers.ModelSerializer):
  status = VehicleStatusSerializer(read_only=True)

  class Meta:
    model = Vehicle
    fields = ['pk','title','status']

#################################################
class VehicleDataSerializer(serializers.ModelSerializer):
  pass

  class Meta:
    model = VehicleData

#################################################
class PinfVehicleSerializer(serializers.ModelSerializer):
  pass

  class Meta:
    model = Vehicle

  def get_identity(self, data):
      """
      This hook is required for bulk update.
      We need to override the default, to use the slug as the identity.

      Note that the data has not yet been validated at this point,
      so we need to deal gracefully with incorrect datatypes.
      """
      try:
          return data.get('carPlate', None)
      except AttributeError:
          return None

  @classmethod
  def create_from_pinf(cls,data):
    properties = data['properties']
    d = {
         'plate': properties['carPlate'],
         'design': properties['carName'],
         'engine': properties['carEngineType'],
         'kind': properties['typeMarker'],
         'agency': properties['carAgency']  
         }
    return cls(cls.get_by_plate(data),data=d, many=False, partial=True)

  @classmethod
  def get_by_plate(cls,data):
    try:
      plate = data['properties']['carPlate']
      return Vehicle.objects.get(plate=plate)
    except Vehicle.DoesNotExist:
      return None
                    
#################################################
class WebstampField(serializers.Field):
  cet_timezone = pytz.timezone('CET')      #timezone locale (CET for CEnTral Europe)
  
  def to_representation(self, obj):
    #18/01/2016 16:05
    return None

  def to_internal_value(self, data):
    #18/01/2016 16:05
    return self.cet_timezone.localize(datetime.strptime(data,"%d/%m/%Y %H:%M"))    

class GeomField(serializers.Field):
  def to_representation(self, obj):
    return obj.geom.json

  def to_internal_value(self, data):
    return GEOSGeometry('POINT ({} {})'.format(data['lng'], data['lat']), srid=4326)

class PinfVehicleDataSerializer(serializers.ModelSerializer):
  webstamp = WebstampField()
  geom = GeomField()

  class Meta:
    model = VehicleData

  @classmethod
  def create_from_pinf(cls,data):
    properties = data['properties']
    d = {
         'vehicle': PinfVehicleSerializer.get_by_plate(data).pk,
         'address': properties['carAddress'],
         'fuel': properties['fuelLevel'],
         'inside': properties['carInsideStatus'],
         'outside': properties['carOutsiteStatus'],
         'webstamp': properties['carUpdate'],
         'geom': {
                  'lat': properties['carLat'],
                  'lng': properties['carLon']
                  }
         }
    return cls(data=d, many=False, partial=True)
