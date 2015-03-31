from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = patterns('',
    ##
    # url(r'^$', 'feinstaub.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url='/v1/', permanent=False)),
    url(r'^v1/', include('sensors.urls')),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
)
