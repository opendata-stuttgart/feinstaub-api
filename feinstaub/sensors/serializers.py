from rest_framework import exceptions, serializers

from .models import (
    Node,
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType,
)


class SensorDataValueSerializer(serializers.ModelSerializer):
    sensordata = serializers.IntegerField(read_only=True,
                                          source='sensordata.pk')

    class Meta:
        model = SensorDataValue
        fields = ('value', 'value_type', 'sensordata')


class SensorDataSerializer(serializers.ModelSerializer):
    sensordatavalues = SensorDataValueSerializer(many=True)
    sensor = serializers.IntegerField(required=False,
                                      source='sensor.pk')

    class Meta:
        model = SensorData
        fields = ('sensor', 'sampling_rate', 'timestamp', 'sensordatavalues')
        read_only = ('location')

    def create(self, validated_data):
        # custom create, because of nested list of sensordatavalues

        # use sensor from authenticator
        successful_authenticator = self.context['request'].successful_authenticator
        if successful_authenticator:
            node, pin = successful_authenticator.authenticate(self.context['request'])
            if node.sensors.count() == 1:
                validated_data['sensor'] = node.sensors.first()
            else:
                validated_data['sensor'] = node.sensors.filter(pin=pin).first()
        else:
            raise exceptions.NotAuthenticated

        if not validated_data['sensor']:
            raise exceptions.ValidationError('sensor could not be selected.')

        sensordatavalues = validated_data.pop('sensordatavalues')

        # set location based on current location of sensor
        validated_data['location'] = node.location
        sd = SensorData.objects.create(**validated_data)

        for value in sensordatavalues:
            # set sensordata to newly created SensorData
            value['sensordata'] = sd
            SensorDataValue.objects.create(**value)

        return sd


class NestedSensorDataValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorDataValue
        fields = ('id', 'value', 'value_type')


class NestedSensorDataSerializer(serializers.ModelSerializer):
    sensordatavalues = NestedSensorDataValueSerializer(many=True)

    class Meta:
        model = SensorData
        fields = ('id', 'sampling_rate', 'timestamp', 'sensordatavalues')
        read_only = ('location')


class NestedSensorLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorLocation
        fields = ('id', "location", "indoor", "description")


class NestedSensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        fields = ('id', "name", "manufacturer")


class NestedSensorSerializer(serializers.ModelSerializer):
    sensor_type = NestedSensorTypeSerializer()
    sensordatas = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = ('id', 'description', 'pin', 'sensor_type', 'sensordatas')

    def get_sensordatas(self, obj):
        sensordatas = SensorData.objects.filter(sensor=obj).order_by('-timestamp')[:2]
        serializer = NestedSensorDataSerializer(instance=sensordatas, many=True)
        return serializer.data


class NodeSerializer(serializers.ModelSerializer):
    sensors = NestedSensorSerializer(many=True)
    location = NestedSensorLocationSerializer()
    last_data_push = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ('id', 'sensors', 'uid', 'owner', 'location', 'last_data_push')

    def get_last_data_push(self, obj):
        x = obj.sensors.order_by('-sensordatas__timestamp')[:1].values_list('sensordatas__timestamp', flat=True)
        return x[0] if x else None


class SensorSerializer(serializers.ModelSerializer):
    sensor_type = NestedSensorTypeSerializer()

    class Meta:
        model = Sensor
        fields = ('id', 'description', 'pin', 'sensor_type')


class VerboseSensorDataSerializer(serializers.ModelSerializer):
    sensordatavalues = NestedSensorDataValueSerializer(many=True)

    class Meta:
        model = SensorData
        fields = ('id', 'sampling_rate', 'timestamp', 'sensordatavalues', 'location', 'sensor')
