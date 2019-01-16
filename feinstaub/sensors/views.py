import datetime
import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.views.generic.edit import FormView

from rest_framework import mixins, viewsets, pagination
from rest_framework.response import Response

from .authentication import OwnerPermission, NodeUidAuthentication
from .serializers import (
    SensorDataSerializer,
    NodeSerializer,
    SensorSerializer,
    VerboseSensorDataSerializer,
    NowSerializer,
)

from .models import (
    Node,
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType,
)
from .forms import AddSensordeviceForm


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostSensorDataView(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """ This endpoint is to POST data from the sensor to the api.
    """
    authentication_classes = (NodeUidAuthentication,)
    permission_classes = tuple()
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
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, )
    filter_class = SensorFilter

    def get_queryset(self):
        if self.request.user.is_authenticated():
            if self.request.user.groups.filter(name="show_me_everything").exists():
                return SensorData.objects.all()
            return SensorData.objects.filter(Q(sensor__node__owner=self.request.user) |
                                             Q(sensor__public=True))
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


class NowView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ Show all sensors active in the last 5 minutes with newest value
    """
    permission_classes = []
    serializer_class = NowSerializer
    queryset = SensorData.objects.none()

    def get_queryset(self):
        now = timezone.now()
#        now = datetime.datetime(2016, 1, 1, 1, 1)
        startdate = now - datetime.timedelta(minutes=5)
        return SensorData.objects.filter(modified__range=[startdate, now])


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


class AddSensordeviceView(LoginRequiredMixin, FormView):
    login_url = '/admin/login/'
    form_class = AddSensordeviceForm
    template_name = 'addsensordevice.html'

    def form_valid(self, form):
        if form.cleaned_data.get('value'):
            # TODO: add logic to write all the data into the database
            pass

            # thing, created = Thing.objects.get_or_create(
            #     field=form.cleaned_data.get('field'),
            #     defaults={'optional_field': form.cleaned_data.get('field2')},
            # )
            # if not created:
            #     messages.add_message(self.request,
            #                          messages.ERROR,
            #                          'an error occurred')
        messages.add_message(self.request, messages.INFO, "not implemented yet.")
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('admin:xxx_create')
