from rest_framework import mixins, viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.cache import cache

from .authentication import SensorUidAuthentication, IsSensorValid
from .serializers import SensorDataSerializer

from .models import (
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType,
)


class SensorDataView(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """ This endpoint is to POST data from the sensor to the api.
    """
    authentication_classes = (SensorUidAuthentication,)
    permission_classes = (IsSensorValid,)
    serializer_class = SensorDataSerializer
    queryset = SensorData.objects.all()


class StatisticsView(viewsets.ViewSet):

    def list(self, request):
        stats = {
            'user': {
                'count': User.objects.count(),
                },
            'sensor': {
                'count': Sensor.objects.count(),
                },
            'sensor_data': {
                'count': SensorData.objects.count(),
            },
            'sensor_data_value': {
                'count': SensorDataValue.objects.count(),
            },
            'sensor_type': {
                'count': SensorType.objects.count(),
                'list': SensorType.objects.order_by('uid').values_list('name', flat=True)
            },
            'location': {
                'count': SensorLocation.objects.count(),
            }
        }
        return Response(stats)

class CacheView(viewsets.ViewSet):

    def list(self, request):
        cache_list = [{key: cache.get(key)} for key in cache.iter_keys("location_cache_*")]

        return Response(cache_list)
