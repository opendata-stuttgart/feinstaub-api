# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url
from .views import (
    NodeView,
    PostSensorDataView,
    SensorDataView,
    SensorView,
    StatisticsView,
)
from main.views import UsersView

router = routers.DefaultRouter()
router.register(r'push-sensor-data', PostSensorDataView, base_name="push-sensor-data")
router.register(r'node', NodeView)
router.register(r'sensor', SensorView)
router.register(r'data', SensorDataView)
router.register(r'statistics', StatisticsView, base_name='statistics')
router.register(r'user', UsersView)


urlpatterns = patterns(
    '',
    url(
        regex=r'^', view=include(router.urls)
    ),
)
