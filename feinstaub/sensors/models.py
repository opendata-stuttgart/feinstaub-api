from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.timezone import now


class SensorType(TimeStampedModel):
    uid = models.SlugField(unique=True)
    name = models.CharField(max_length=1000)
    manufacturer = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.uid


class Sensor(TimeStampedModel):
    uid = models.SlugField(unique=True)
    owner = models.ForeignKey(User)
    sensor_type = models.ForeignKey(SensorType)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey("SensorLocation")

    def __str__(self):
        return self.uid


class SensorData(TimeStampedModel):
    sensor = models.ForeignKey(Sensor)
    sampling_rate = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)
    location = models.ForeignKey("SensorLocation", blank=True)

    # in save set location

    def __str__(self):
        return "{sensor}: {value}".format(
            sensor=self.sensor, value=self.value1)


class SensorDataValue(TimeStampedModel):
    sensordata = models.ForeignKey(SensorData)
    value = models.TextField()
    value_type = models.CharField(max_length=100, choices=(
        ('P1', '1µm particles'),
        ('P2', '2.5µm particles'),
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('brightness', 'Brightness'),
    ))


class SensorLocation(TimeStampedModel):
    location = models.TextField(null=True, blank=True)
    # FIXME: geofield for lat/lon
    indoor = models.BooleanField()
    owner = models.ForeignKey(User, null=True, blank=True,
                              help_text="If not set, location is public.")
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "{location}".format(location=self.location)
