from django.conf.urls import url, include

from .views import position


position_patterns = [
    url(r'^$', position.List.as_view(), name='position-list'),
    url(r'^create/$', position.Create.as_view(), name='position-create'),
    url(r'^(?P<position_id>[A-Za-z0-9]+)/$', position.Update.as_view(),
        name='position-update'),
    url(r'^(?P<position_id>[A-Za-z0-9]+)/delete/$', position.Delete.as_view(),
        name='position-delete'),
]


urlpatterns = [
    url(r'^projects/(?P<project_id>[A-Za-z0-9]+)/positions/',
        include(position_patterns))
]
