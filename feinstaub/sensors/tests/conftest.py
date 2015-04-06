import pytest

from sensors.models import Sensor, SensorLocation, SensorType

PASSWORD = 'secret'
EMAIL = 'test@example.com'
USERNAME = 'Test User'


@pytest.fixture
def logged_in_user():
    from django.contrib.auth import get_user_model
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=USERNAME, email=EMAIL, password=PASSWORD
    )
    user.set_password(PASSWORD)
    user.save()

    from rest_framework.authtoken.models import Token
    Token.objects.create(user=user)

    return user


@pytest.fixture
def location():
    l, x = SensorLocation.objects.get_or_create(description='somewhere')
    return l


@pytest.fixture
def sensor_type():
    st, x = SensorType.objects.get_or_create(uid="A", name="B",
                                             manufacturer="C")
    return st


@pytest.fixture
def sensor(logged_in_user, sensor_type, location):
    s, x = Sensor.objects.get_or_create(uid='test123',
                                        owner=logged_in_user,
                                        sensor_type=sensor_type,
                                        location=location)
    return s
