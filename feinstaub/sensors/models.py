from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.timezone import now


class SensorType(TimeStampedModel):
    uid = models.SlugField(unique=True)
    name = models.CharField(max_length=1000)
    manufacturer = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000, null=True, blank=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.uid


class Node(TimeStampedModel):
    uid = models.SlugField(unique=True)
    owner = models.ForeignKey(User)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey("SensorLocation")

    class Meta:
        ordering = ['uid', ]

    def __str__(self):
        return self.uid


class Sensor(TimeStampedModel):
    node = models.ForeignKey(Node, related_name="sensors")
    pin = models.CharField(max_length=10, default="-",
                           help_text="differentiate the sensors on one node by giving pin used")
    sensor_type = models.ForeignKey(SensorType)
    description = models.TextField(null=True, blank=True)
    public = models.BooleanField(default=False)

    class Meta:
        unique_together = ('node', 'pin')

    def __str__(self):
        return "{} {}".format(self.node, self.pin)


class SensorData(TimeStampedModel):
    sensor = models.ForeignKey(Sensor, related_name="sensordatas")
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
    ##
    ('door_state', 'door state (open/closed)'),
)


class SensorDataValue(TimeStampedModel):

    sensordata = models.ForeignKey(SensorData, related_name='sensordatavalues')
    value = models.TextField(db_index=True)
    value_type = models.CharField(max_length=100, choices=SENSOR_TYPE_CHOICES,
                                  db_index=True)

    def __str__(self):
        return "{sensordata}: {value} [{value_type}]".format(
            sensordata=self.sensordata,
            value=self.value,
            value_type=self.value_type,
        )


class SensorLocation(TimeStampedModel):
    location = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=11, null=True, blank=True)
    indoor = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, blank=True,
                              help_text="If not set, location is public.")
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    class Meta:
        ordering = ['location', ]

    def __str__(self):
        return "{location}".format(location=self.location)
