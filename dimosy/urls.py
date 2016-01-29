from django.contrib import admin
from django.conf.urls import include, url

# urlpatterns = patterns('',
#                        # Examples:
#                        # url(r'^$', 'dimosy4.views.home', name='home'),
#                        # url(r'^blog/', include('blog.urls')),
#                        url(r'^tachy/', include('tachy.urls')),
#                        url(r'^admin/', include(admin.site.urls)),
#                        # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#                        )

urlpatterns = [
    url(r'^sensors/tachy/', include('sensors.tachy.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
