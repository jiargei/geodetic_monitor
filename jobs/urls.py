from django.conf.urls import url, include

from .views import tasks


task_patterns = [
    url(r'^$', tasks.List.as_view(), name='task-list'),
    url(r'^create/$', tasks.Create.as_view(), name='task-create'),
    url(r'^(?P<task_id>[A-Za-z0-9]+)/$', tasks.Update.as_view(),
        name='task-update'),
    url(r'^(?P<task_id>[A-Za-z0-9]+)/delete/$', tasks.Delete.as_view(),
        name='task-delete'),
]

urlpatterns = [
    url(r'^projects/(?P<project_id>[A-Za-z0-9]+)/jobs/',
        include(task_patterns)),
]
