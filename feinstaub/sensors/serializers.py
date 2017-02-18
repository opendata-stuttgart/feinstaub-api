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
        fields = ('sensor', 'sampling_rate', 'timestamp', 'sensordatavalues', 'software_version')
        read_only = ('location')

    def create(self, validated_data):
        # custom create, because of nested list of sensordatavalues

        sensordatavalues = validated_data.pop('sensordatavalues', [])
        if not sensordatavalues:
            raise exceptions.ValidationError('sensordatavalues was empty. Nothing to save.')

        # use sensor from authenticator
        successful_authenticator = self.context['request'].successful_authenticator
        if not successful_authenticator:
            raise exceptions.NotAuthenticated

        node, pin = successful_authenticator.authenticate(self.context['request'])
        if node.sensors.count() == 1:
            sensors_qs = node.sensors.all()
        else:
            sensors_qs = node.sensors.filter(pin=pin)
        sensor_id = sensors_qs.values_list('pk', flat=True).first()

        if not sensor_id:
            raise exceptions.ValidationError('sensor could not be selected.')
        validated_data['sensor_id'] = sensor_id

        # set location based on current location of sensor
        validated_data['location'] = node.location
        sd = SensorData.objects.create(**validated_data)

        SensorDataValue.objects.bulk_create(
            SensorDataValue(
                sensordata_id=sd.pk,
                **value,
            )
            for value in sensordatavalues
        )

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
        return obj.sensors \
            .order_by('-sensordatas__timestamp') \
            .values_list('sensordatas__timestamp', flat=True) \
            .first()


class SensorSerializer(serializers.ModelSerializer):
    sensor_type = NestedSensorTypeSerializer()

    class Meta:
        model = Sensor
        fields = ('id', 'description', 'pin', 'sensor_type')


class VerboseSensorDataSerializer(serializers.ModelSerializer):
    sensordatavalues = NestedSensorDataValueSerializer(many=True)

    class Meta:
        model = SensorData
        fields = ('id', 'sampling_rate', 'timestamp', 'sensordatavalues', 'location', 'sensor', 'software_version')


# ##################################################


class NowSensorSerializer(serializers.ModelSerializer):
    sensor_type = NestedSensorTypeSerializer()

    class Meta:
        model = Sensor
        fields = ('id', 'pin', 'sensor_type')


class NowSensorLocationSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=6, decimal_places=3)
    longitude = serializers.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        model = SensorLocation
        fields = ('id', 'latitude', 'longitude')


class NowSerializer(serializers.ModelSerializer):
    location = NowSensorLocationSerializer()
    sensor = NowSensorSerializer()
    sensordatavalues = NestedSensorDataValueSerializer(many=True)

    class Meta:
        model = SensorData
        fields = ('id', 'sampling_rate', 'timestamp', 'sensordatavalues', 'location', 'sensor')
