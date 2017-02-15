from rest_framework import authentication
from rest_framework import permissions
from rest_framework import exceptions

from .models import Node, SensorData


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
        if hasattr(obj, 'sensordata'):
            obj = obj.sensordata
        if hasattr(obj, 'sensor'):
            obj = obj.sensor
        if hasattr(obj, 'node'):
            obj = obj.node
        return request.user == obj.owner
