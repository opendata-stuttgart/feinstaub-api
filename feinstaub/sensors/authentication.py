from rest_framework import authentication
from rest_framework import permissions
from rest_framework import exceptions

from .models import Node, Sensor, SensorData, SensorDataValue


class NodeUidAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        node_uid = request.META.get('HTTP_X_SENSOR') or request.META.get('HTTP_SENSOR') or request.META.get('HTTP_NODE')
        if not node_uid:
            return None

        node_pin = request.META.get('HTTP_X_PIN') or request.META.get('HTTP_PIN', '-')

        try:
            node = Node.objects.get(uid=node_uid)
        except Node.DoesNotExist:
            raise exceptions.AuthenticationFailed('Node not found in database.')

        return (node, node_pin)


class OwnerPermission(permissions.BasePermission):
    """Checks if authenticated user is owner of the node"""

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, SensorDataValue):
            owner_pk = SensorDataValue.objects \
                .filter(pk=obj.pk) \
                .values_list('sensordata__sensor__node__owner_id', flat=True) \
                .first()
        elif isinstance(obj, SensorData):
            owner_pk = SensorData.objects \
                .filter(pk=obj.pk) \
                .values_list('sensor__node__owner_id', flat=True) \
                .first()
        elif isinstance(obj, Sensor):
            owner_pk = Sensor.objects \
                .filter(pk=obj.pk) \
                .values_list('node__owner_id', flat=True) \
                .first()
        elif isinstance(obj, Node):
            owner_pk = obj.owner_id
        else:
            return False

        return request.user.pk == owner_pk
