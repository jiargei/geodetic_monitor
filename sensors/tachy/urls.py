from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'control.html', views.TachyControlView.as_view(), name='control'),
]
