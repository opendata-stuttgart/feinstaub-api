# coding=utf-8
from rest_framework import routers
from django.conf.urls import patterns, include, url


router = routers.DefaultRouter()


urlpatterns = patterns(
    '',
    url(
        regex=r'^', view=include(router.urls)
    ),
)
