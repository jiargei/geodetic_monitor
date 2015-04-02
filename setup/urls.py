from django.conf.urls import url, include
from setup.views import ProjectViewSet, TachyPositionViewSet, TachyStationViewSet
from setup.views import FipoTargetViewSet, FipoMeasurementViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_nested import routers

# Create URLs here

project_router = DefaultRouter()
project_router.register(r'projects', ProjectViewSet)

tachy_position_router = routers.NestedSimpleRouter(project_router, r'projects', lookup='projects')
tachy_position_router.register(r'tachypositions', TachyPositionViewSet)

tachy_station_router = routers.NestedSimpleRouter(tachy_position_router, r'tachypositions', lookup='tachypositions')
tachy_station_router.register(r'stations', TachyStationViewSet)

fipo_target_router = routers.NestedSimpleRouter(project_router, r'projects', lookup='projects')
fipo_target_router.register(r'fipotargets', FipoTargetViewSet)

fipo_target_measurement_router = routers.NestedSimpleRouter(fipo_target_router, r'fipotargets', lookup='fipotargets')
fipo_target_measurement_router.register(r'measurements', FipoMeasurementViewSet)

fipo_station_measurement_router = routers.NestedSimpleRouter(tachy_station_router, r'stations', lookup='stations')
fipo_station_measurement_router.register(r'fipomeasurements', FipoMeasurementViewSet)

# The API URLs are now determined automatically by the router.

urlpatterns = [
    url(r'^', include(project_router.urls)),
    url(r'^', include(tachy_position_router.urls)),
    url(r'^', include(tachy_station_router.urls)),
    url(r'^', include(fipo_target_router.urls)),
    url(r'^', include(fipo_target_measurement_router.urls)),
    url(r'^', include(fipo_station_measurement_router.urls)),
]
