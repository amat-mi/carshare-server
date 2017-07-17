# coding: utf-8

from django.contrib import admin

from models import Agency, Vehicle
from carshare.models import Authorization


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

#################################################
class AuthorizationAdmin(BaseAdmin):
  def agency_title(self, obj):
    return obj.agency.title
  agency_title.short_description = 'Agenzia'
  
  list_display = ('plate','agency_title','fromstamp','tostamp','is_active',)
  search_fields = ('plate','agency__title',)  
admin.site.register(Authorization,AuthorizationAdmin)
