from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from setup import views as sv
from tachy_control import views as tc
from users.views import UserViewSet

router = DefaultRouter()

# The API URLs are now determined automatically by the router.

router.register(r'tachypositions', sv.TachyPositionViewSet)
router.register(r'tachystations', sv.TachyStationViewSet)
router.register(r'fipotargets', sv.FipoTargetViewSet)
router.register(r'fipotasks', sv.FipoTaskViewSet)
router.register(r'fipomeasurements', sv.FipoMeasurementViewSet)
router.register(r'supotargets', sv.SupoTargetViewSet)
router.register(r'supotasks', sv.SupoTaskViewSet)
router.register(r'supomeasurements', sv.SupoMeasurementViewSet)

router.register(r'tachysensors', tc.TachySensorViewSet)

router.register(r'users', UserViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dimosy4.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(router.urls)),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tachy_control.urls')),
    url(r'^', include('setup.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
