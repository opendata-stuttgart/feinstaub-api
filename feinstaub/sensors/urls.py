# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url
from .views import SensorDataView, StatisticsView, CacheView, KindleView


router = routers.DefaultRouter()
router.register(r'push-sensor-data', SensorDataView)
router.register(r'statistics', StatisticsView, base_name='statistics')
router.register(r'cache', CacheView, base_name='cache')
router.register(r'kindle', KindleView, base_name='kindle')


urlpatterns = patterns(
    '',
    url(
        regex=r'^', view=include(router.urls)
    ),
)
