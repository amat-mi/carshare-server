# coding: utf-8

from django.contrib.gis.db import models as geomodels
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


#################################################
class Status(models.Model):
  address = models.CharField(max_length=120, null=True, blank=True)
  fuel = models.IntegerField(null=True, blank=True)
  inside = models.IntegerField(null=True, blank=True)
  outside = models.IntegerField(null=True, blank=True)
  stamp = models.DateTimeField(null=False, auto_now_add=True)
  webstamp = models.DateTimeField(null=True,blank=True)
  geom = geomodels.PointField(srid=4326, null=True, blank=True)
  objects = geomodels.GeoManager() # so we can use spatial queryset methods

  class Meta:
    ordering = ['stamp']
    abstract = True

#################################################
class VehicleData(Status):
  vehicle = models.ForeignKey('Vehicle', related_name='data', null=False, on_delete=models.CASCADE)  

  class Meta:
    verbose_name = "Dati veicolo"
    verbose_name_plural = "Dati veicoli"
    ordering = ['vehicle','stamp']

@receiver(post_save, sender=VehicleData)
def post_save_VehicleData(sender, instance, created, *args, **kwargs):
  u"""
  Dopo la creazione di un dato di veicolo, chiama la refresh sul veicolo per ricalcolare lo status corrente 
  """
  if created:
    instance.vehicle.update_status(instance)        

#################################################
class VehicleStatus(Status):
  vehicle = models.OneToOneField('Vehicle', related_name='status', null=False, on_delete=models.CASCADE)  

  class Meta:
    verbose_name = "Stato veicolo"
    verbose_name_plural = "Stato veicoli"
    ordering = ['vehicle','stamp']

  def copy_from_vehicledata(self,vehicledata):
    self.address = vehicledata.address
    self.fuel = vehicledata.fuel
    self.inside = vehicledata.inside
    self.outside = vehicledata.outside
    self.stamp = vehicledata.stamp
    self.webstamp = vehicledata.webstamp
    self.geom = vehicledata.geom
    self.vehicle = vehicledata.vehicle    
    self.full_clean()
    self.save()    

#################################################
class Agency(models.Model):
  id = models.IntegerField(primary_key=True)
  title = models.CharField(max_length=40, null=False, unique=True)
  url = models.URLField(max_length=120, null=True, blank=True)

  def __unicode__(self):
    return u'{} - {}'.format(self.id,self.title)  
  
  class Meta:
    verbose_name = "Agenzia"
    verbose_name_plural = "Agenzie"
    ordering = ['id','title']
  
#################################################
class Vehicle(models.Model):
  plate = models.CharField(max_length=20, null=False, unique=True)
  design = models.CharField(max_length=40, null=False,blank=True,default='Unknown')
  engine = models.CharField(max_length=20, null=True,blank=True)
  kind = models.CharField(max_length=20, null=True,blank=True)
  agency = models.ForeignKey('Agency', related_name='vehicles', null=False, on_delete=models.CASCADE)  
  
  def __unicode__(self):
    return u'{} - {}'.format(self.plate,self.design)  
  
  class Meta:
    verbose_name = "Veicolo"
    verbose_name_plural = "Veicoli"
    ordering = ['plate']

  def update_status(self,vehicledata):
    try:
      status = self.status
    except ObjectDoesNotExist:
      status = VehicleStatus()
    status.copy_from_vehicledata(vehicledata)
    status.full_clean()
    status.save()    
    self.status = status
    self.full_clean()
    self.save()    
