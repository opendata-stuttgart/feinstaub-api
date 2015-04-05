from rest_framework import mixins, viewsets

from .authentication import SensorUidAuthentication, IsSensorValid
from .serializers import SensorDataSerializer
from .models import SensorData


class SensorDataView(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    """ This endpoint is to POST data from the sensor to the api.
    """
    authentication_classes = (SensorUidAuthentication,)
    permission_classes = (IsSensorValid,)
    serializer_class = SensorDataSerializer
    queryset = SensorData.objects.all()
