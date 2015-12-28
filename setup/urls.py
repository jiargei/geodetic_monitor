from django.conf.urls import url, patterns
from . import views

urlpatterns = [
    url(r'tachy-control/$', views.TachyControlView.as_view(), name='tachy-control'),
]
