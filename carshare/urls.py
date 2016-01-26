# coding: utf-8

from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from views import VehicleViewSet, VehicleDataViewSet


router = SimpleRouter()

##### Elenco endpoints ################################
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicledata', VehicleDataViewSet)


##### Aggiunta degli url ####################################
urlpatterns =  patterns('',
    url(r'^', include(router.urls)),    
)
