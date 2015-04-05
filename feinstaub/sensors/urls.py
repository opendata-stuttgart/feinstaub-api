# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url
from .views import SensorDataView


router = routers.DefaultRouter()
router.register(r'sensor-data', SensorDataView)


urlpatterns = patterns(
    '',
    url(
        regex=r'^', view=include(router.urls)
    ),
)
