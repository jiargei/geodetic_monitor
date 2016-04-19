from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home.html'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^', include('metering.urls')),
    url(r'^', include('jobs.urls')),
]
