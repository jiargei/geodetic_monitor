
from django.conf.urls import url, include
from tachy_control import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
tachy_router = DefaultRouter()
tachy_router.register(r'tachysensors', views.TachySensorViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(tachy_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
