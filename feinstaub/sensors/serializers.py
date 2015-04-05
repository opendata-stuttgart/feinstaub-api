from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import SensorData, SensorDataValue


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

        sensordatavalues = validated_data.pop('sensordatavalues')

        # set location based on current location of sensor
        validated_data['location'] = validated_data['sensor'].location
        sd = SensorData.objects.create(**validated_data)

        for value in sensordatavalues:
            # set sensordata to newly created SensorData
            value['sensordata'] = sd
            SensorDataValue.objects.create(**value)

        return sd
