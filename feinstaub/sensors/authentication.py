from rest_framework import authentication
from rest_framework import permissions
from rest_framework import exceptions

from .models import Sensor, SensorData


class IsSensorValid(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # sensor has owner
        # owner can not be checked, because the sensor push has
        # no SessionAuthentication or TokenAuthentication
        if isinstance(obj, SensorData):
            obj = obj.sensor
        if hasattr(obj, 'owner'):
            return obj.owner is not None
        return None


class SensorUidAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        sensor_uid = request.META.get('HTTP_SENSOR')
        if not sensor_uid:
            return None

        try:
            sensor = Sensor.objects.get(uid=sensor_uid)
        except Sensor.DoesNotExist:
            raise exceptions.AuthenticationFailed('Sensor not found in database.')

        return (sensor, None)
