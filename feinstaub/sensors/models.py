from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


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
    description = models.CharField(max_length=10000)

    def __str__(self):
        return self.uid


class SensorData(TimeStampedModel):
    sensor = models.ForeignKey(Sensor)
    # values are integer for now.
    # when first sensor is added that wants decimal, we will add a field for that
    value1 = models.IntegerField()
    value2 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{sensor}: {value}".format(
            sensor=self.sensor, value=self.value1)


class SensorLocation(TimeStampedModel):
    sensor = models.ForeignKey(Sensor)
    location = models.TextField(null=True, blank=True)
    # FIXME: geofield for lat/lon

    def __str__(self):
        return "{sensor}: {location}".format(
            sensor=self.sensor, location=self.location)
