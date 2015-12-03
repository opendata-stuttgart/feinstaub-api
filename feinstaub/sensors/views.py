import django_filters
from django.contrib.auth.models import User
from rest_framework import mixins, viewsets, filters, pagination
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


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.request.user.is_authenticated():
            if self.request.user.groups.filter(name="show_me_everything").exists():
                return Sensor.objects.all()
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
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = SensorFilter

    def get_queryset(self):
        if self.request.user.is_authenticated():
            if self.request.user.groups.filter(name="show_me_everything").exists():
                return SensorData.objects.all()
            return SensorData.objects.filter(sensor__node__owner=self.request.user)
        return SensorData.objects.filter(sensor__public=True)


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
            if self.request.user.groups.filter(name="show_me_everything").exists():
                return Node.objects.all()
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
