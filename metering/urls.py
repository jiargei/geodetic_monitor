from django.conf.urls import url, include

from .views import position, target


position_patterns = [
    url(r'^$', position.List.as_view(), name='position-list'),
    url(r'^create/$', position.Create.as_view(), name='position-create'),
    url(r'^(?P<position_id>[A-Za-z0-9]+)/$', position.Update.as_view(),
        name='position-update'),
    url(r'^(?P<position_id>[A-Za-z0-9]+)/delete/$', position.Delete.as_view(),
        name='position-delete'),
]
target_patterns = [
    url(r'^$', target.List.as_view(), name='target-list'),
    url(r'^create/$', target.Create.as_view(), name='target-create'),
    url(r'^(?P<target_id>[A-Za-z0-9]+)/$', target.Update.as_view(),
        name='target-update'),
    url(r'^(?P<target_id>[A-Za-z0-9]+)/delete/$', target.Delete.as_view(),
        name='target-delete'),
]

urlpatterns = [
    url(r'^projects/(?P<project_id>[A-Za-z0-9]+)/positions/',
        include(position_patterns)),
     url(r'^projects/(?P<project_id>[A-Za-z0-9]+)/targets/',
        include(target_patterns))
]
