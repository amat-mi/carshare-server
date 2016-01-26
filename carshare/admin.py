# coding: utf-8

from django.contrib import admin

from models import Agency, Vehicle


#################################################
class BaseAdmin(admin.ModelAdmin):
  save_on_top = True    

#################################################
class AgencyAdmin(BaseAdmin):
  pass
admin.site.register(Agency,AgencyAdmin)

#################################################
class VehicleAdmin(BaseAdmin):
  pass
admin.site.register(Vehicle,VehicleAdmin)
