# coding=utf-8
from rest_framework.test import APIRequestFactory
import pytest

from sensors.views import PostSensorDataView


@pytest.mark.django_db
class TestAuthenticator:

    @pytest.fixture(params=[
        # uid, status_code
        ['test123', 201],
        ##########
        ['INVALID', 403],
        ])
    def authenticator_fixture(self, request):
        keys = ["uid", "status_code"]
        return dict(zip(keys, request.param))

    def test_sensoruid_authenticator(self, sensor, authenticator_fixture):
        factory = APIRequestFactory()
        view = PostSensorDataView
        url = '/v1/push-sensor-data/'
        request = factory.post(url, {'sensordatavalues': [{"value": 10, "value_type": "P1"}], },
                               format='json')

        # set HTTP header the same way the client would do
        request.META['HTTP_SENSOR'] = authenticator_fixture.get('uid')

        view_function = view.as_view({'post': 'create'})
        response = view_function(request)

        assert response.status_code == authenticator_fixture.get('status_code')
