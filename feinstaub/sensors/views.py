from rest_framework import mixins, viewsets

from .serializers import SensorDataSerializer
from .models import SensorData, SensorDataValue


class SensorDataView(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """ This endpoint is to POST data from the sensor to the api.
    """
#    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SensorDataSerializer
    queryset = SensorData.objects.all()
