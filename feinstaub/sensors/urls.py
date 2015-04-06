# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url
from .views import SensorDataView, StatisticsView


router = routers.DefaultRouter()
router.register(r'push-sensor-data', SensorDataView)
router.register(r'statistics', StatisticsView, base_name='statistics')


urlpatterns = patterns(
    '',
    url(
        regex=r'^', view=include(router.urls)
    ),
)
