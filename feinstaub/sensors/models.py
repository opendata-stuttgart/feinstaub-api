from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.timezone import now


class SensorType(TimeStampedModel):
    uid = models.SlugField(unique=True)
    name = models.CharField(max_length=1000)
    manufacturer = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000, null=True, blank=True)

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
    sampling_rate = models.IntegerField(null=True, blank=True,
                                        help_text="in milliseconds")
    timestamp = models.DateTimeField(default=now)
    location = models.ForeignKey("SensorLocation", blank=True)

    def __str__(self):
        return "{sensor} [{value_count}]".format(
            sensor=self.sensor, value_count=self.sensordatavalues.count())


SENSOR_TYPE_CHOICES = (
    # ppd42ns
    ('P1', '1µm particles'),
    ('P2', '2.5µm particles'),
    ('durP1', 'duration 1µm'),
    ('durP2', 'duration 2.5µm'),
    ('ratioP1', 'ratio 1µm in percent'),
    ('ratioP2', 'ratio 2.5µm in percent'),
    # sht10-sht15; dht11, dht22; bmp180
    ('temperature', 'Temperature'),
    # sht10-sht15; dht11, dht22
    ('humidity', 'Humidity'),
    # bmp180
    ('pressure', 'Pa'),
    ('altitude', 'meter'),
    ('pressure_sealevel', 'Pa (sealevel)'),
    #
    ('brightness', 'Brightness'),
    # gp2y10
    ('dust_density', 'Dust density in mg/m3'),
    ("vo_raw", 'Dust voltage raw'),
    ("voltage", "Dust voltage calculated"),
    # dsm501a
    ('P10', '1µm particles'),   # identical to P1
    ('P25', '2.5µm particles'),  # identical to P2
    ('durP10', 'duration 1µm'),
    ('durP25', 'duration 2.5µm'),
    ('ratioP10', 'ratio 1µm in percent'),
    ('ratioP25', 'ratio 2.5µm in percent'),
)


class SensorDataValue(TimeStampedModel):

    sensordata = models.ForeignKey(SensorData, related_name='sensordatavalues')
    value = models.TextField()
    value_type = models.CharField(max_length=100, choices=SENSOR_TYPE_CHOICES)

    def __str__(self):
        return "{sensordata}: {value} [{value_type}]".format(
            sensordata=self.sensordata,
            value=self.value,
            value_type=self.value_type,
        )


class SensorLocation(TimeStampedModel):
    location = models.TextField(null=True, blank=True)
    # FIXME: geofield for lat/lon
    indoor = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True,
                              help_text="If not set, location is public.")
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "{location}".format(location=self.location)
