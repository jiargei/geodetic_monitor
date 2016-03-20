from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from . import views


project_patterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name='accounts/project_list.html')),
        name='project-list'),
    url(r'^(?P<project_id>[A-Za-z0-9]+)/$', views.ProjectDetail.as_view(),
        name='project-detail')
]


urlpatterns = [
    url(r'^projects/', include(project_patterns)),
]
