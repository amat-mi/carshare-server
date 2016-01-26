# coding: utf-8

from datetime import date

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

  def is_different_from(self,instance):
    u"""    
    Confronta i miei dati con quelli dell'istanza specificata e ritorna True se è None, 
    oppure se almeno uno dei campi è diverso (a parte stamp e webstamp), o se sono relativi ad un giorno diverso.
    """
    if not instance: return True                  #se istanza non specificata, è comunque diversa
    if not instance.webstamp: return True         #se istanza senza webstamp, è comunque diversa
    if self.address != instance.address: return True
    if self.fuel != instance.fuel: return True
    if self.inside != instance.inside: return True
    if self.outside != instance.outside: return True
    if self.geom != instance.geom: return True
    return self.webstamp.date() != date.today()

#################################################
class VehicleData(Status):
  vehicle = models.ForeignKey('Vehicle', related_name='data', null=False, on_delete=models.CASCADE)  

  class Meta:
    verbose_name = "Dati veicolo"
    verbose_name_plural = "Dati veicoli"
    ordering = ['vehicle','stamp']

  def save(self, *args, **kwargs):
    u"""
    Salvo l'istanza solo se il Vehicle a cui appartiene lo richiede.
    """
    if(self.vehicle.should_save_data(self)):
      super(VehicleData, self).save(*args, **kwargs)

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

  def should_save_data(self,vehicledata):
    u"""
    I dati specificati devono essere salvati solo se non ne esistono (Vehicle senza VehicleStatus),
    oppure se sono diversi dal VehicleStatus corrente, oppure se sono relativi ad un giorno diverso.
    """
    try:
      return self.status.is_different_from(vehicledata)      
    except ObjectDoesNotExist:
      return True         #se non esiste lo status, bisogna salvare i nuovi dati      
    
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
