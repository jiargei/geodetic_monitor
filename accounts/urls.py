from django.conf.urls import url, include
from django.views.generic import TemplateView


project_patterns = [
    url(r'^$', TemplateView.as_view(template_name='accounts/project_list.html'),
        name='project-list'),
]


urlpatterns = [
    url(r'^projects/', include(project_patterns)),
]
