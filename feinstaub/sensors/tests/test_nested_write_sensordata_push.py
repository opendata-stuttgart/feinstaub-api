# coding=utf-8
from rest_framework.test import APIRequestFactory
import pytest

from sensors.views import PostSensorDataView


@pytest.mark.django_db
class TestSensorDataPush:

    @pytest.fixture(params=[
        # value, status_code, count
        [[], 201, 0],
        [[{"value": 10, "value_type": "P1"}], 201, 1],
        [[{"value": 10, "value_type": "P1"}, {"value": 99, "value_type": "P2"}], 201, 2],
        ## failes:
        ['INVALID', 400, 1],
        [['INVALID'], 400, 1],
        [[{'INVALID_KEY': 1}], 400, 1],
        ])
    def sensordatavalue_fixture(self, request):
        keys = ["value", "status_code", "count"]
        return dict(zip(keys, request.param))

    def test_sensordata_push(self, sensor, sensordatavalue_fixture):
        factory = APIRequestFactory()
        view = PostSensorDataView
        url = '/v1/push-sensor-data/'
        request = factory.post(url, {'sensordatavalues':
                                     sensordatavalue_fixture.get('value'), },
                               format='json')

        # FIXME: test for HTTP_NODE
        request.META['HTTP_SENSOR'] = sensor.node.uid

        view_function = view.as_view({'post': 'create'})
        response = view_function(request)

        assert len(response.data.get('sensordatavalues')) ==\
            sensordatavalue_fixture.get('count')

        assert response.status_code ==\
            sensordatavalue_fixture.get('status_code')
