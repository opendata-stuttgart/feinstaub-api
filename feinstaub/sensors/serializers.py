from rest_framework import exceptions, serializers

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

        # use sensor from authenticator
        successful_authenticator = self.context['request'].successful_authenticator
        if successful_authenticator:
            node, x = successful_authenticator.authenticate(self.context['request'])
            if node.sensor_set.count() == 1:
                validated_data['sensor'] = node.sensor_set.first()
            else:
                # FIXME get pin somehow. think about that!!
                pass
        else:
            raise exceptions.NotAuthenticated

        sensordatavalues = validated_data.pop('sensordatavalues')

        # set location based on current location of sensor
        validated_data['location'] = validated_data['sensor'].location
        sd = SensorData.objects.create(**validated_data)

        for value in sensordatavalues:
            # set sensordata to newly created SensorData
            value['sensordata'] = sd
            SensorDataValue.objects.create(**value)

        return sd
