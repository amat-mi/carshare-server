# coding: utf-8

from django.urls import re_path as url, include
from rest_framework.routers import SimpleRouter

from .views import VehicleViewSet, VehicleDataViewSet


router = SimpleRouter()

##### Elenco endpoints ################################
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicledata', VehicleDataViewSet)


##### Aggiunta degli url ####################################
app_name = 'carshare'
urlpatterns =  [
    url(r'^', include(router.urls)),    
]
