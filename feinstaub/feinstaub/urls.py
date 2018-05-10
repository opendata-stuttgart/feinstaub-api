
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls.static import static


from django.conf import settings


from sensors.views import AddSensordeviceView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', RedirectView.as_view(url='/v1/', permanent=False)),
    url(r'^v1/', include('sensors.urls')),
    url(r'^auth/', include('rest_framework.urls',
                           namespace='rest_framework')),
    url(r'^get-auth-token/', obtain_auth_token),
    url(r'^adddevice/', AddSensordeviceView.as_view(), name='adddevice'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
