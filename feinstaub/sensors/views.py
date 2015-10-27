import django_filters
from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, filters
from rest_framework.response import Response

from .authentication import IsSensorValid, OwnerPermission, NodeUidAuthentication
from .serializers import (
    SensorDataSerializer,
    NodeSerializer,
    SensorSerializer,
    VerboseSensorDataSerializer,
)

from .models import (
    Node,
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType,
)


class PostSensorDataView(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """ This endpoint is to POST data from the sensor to the api.
    """
    authentication_classes = (NodeUidAuthentication,)
    permission_classes = (IsSensorValid,)
    serializer_class = SensorDataSerializer
    queryset = SensorData.objects.all()


class SensorView(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """ This endpoint is to download sensor data from the api.
    """
    permission_classes = (OwnerPermission,)
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Sensor.objects.filter(node__owner=self.request.user)
        return Sensor.objects.none()


class SensorFilter(django_filters.FilterSet):
    # allows timestamps like: 2015-09-19T23:20:15.702705Z
    timestamp_newer = django_filters.IsoDateTimeFilter(name="timestamp", lookup_type='gte')

    class Meta:
        model = SensorData
        fields = ['timestamp_newer', 'sensor']


class SensorDataView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """ This endpoint is to download sensor data from the api.
    """
    permission_classes = (OwnerPermission,)
    serializer_class = VerboseSensorDataSerializer
    queryset = SensorData.objects.all()
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = SensorFilter

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return SensorData.objects.filter(sensor__node__owner=self.request.user)
        return SensorData.objects.none()


class NodeView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               viewsets.GenericViewSet):
    """ Show all nodes belonging to authenticated user
    """
    permission_classes = (OwnerPermission,)
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Node.objects.filter(owner=self.request.user)
        return Node.objects.none()


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
