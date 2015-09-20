# coding=utf-8
from rest_framework.test import APIRequestFactory
import pytest
import pytz

from sensors.views import PostSensorDataView
from sensors.models import SensorData


@pytest.mark.django_db
class TestSensorDataPushFull:

    @pytest.fixture
    def data_fixture(self):
        return {
            "sampling_rate": "15000",
            "timestamp": "2015-04-05 22:10:10+02:00",
            "sensordatavalues": [{"value": 10, "value_type": "P1"},
                                 {"value": 99, "value_type": "P2"}]
        }

    def test_full_data_push(self, sensor, data_fixture):
        factory = APIRequestFactory()
        view = PostSensorDataView
        url = '/v1/push-sensor-data/'
        request = factory.post(url, data_fixture,
                               format='json')

        # authenticate sensor
        request.META['HTTP_SENSOR'] = sensor.node.uid
        # FIXME: test for HTTP_NODE

        view_function = view.as_view({'post': 'create'})
        response = view_function(request)

        assert response.status_code == 201

        sd = SensorData.objects.get(sensor=response.data['sensor'])

        assert sd.sensordatavalues.count() == 2
        assert sd.sensordatavalues.get(value_type="P1").value ==\
            str(data_fixture['sensordatavalues'][0]['value'])
        assert sd.sensordatavalues.get(value_type="P2").value ==\
            str(data_fixture['sensordatavalues'][1]['value'])

        assert sd.location == sensor.node.location

        cest = pytz.timezone('Europe/Berlin')
        assert str(cest.normalize(sd.timestamp)) == data_fixture['timestamp']
