# coding=utf-8
import os
import datetime
from itertools import product

from django.core.management import BaseCommand


def str2date(str, default):
    return datetime.datetime.strptime(str, '%Y-%m-%d').date() if str else default


class Command(BaseCommand):

    help = "Dump all Sensordata to csv files"

    def add_arguments(self, parser):
        parser.add_argument('--start_date')
        parser.add_argument('--end_date')
        parser.add_argument('--type')
        parser.add_argument('--no_excludes', action="store_false")

    def handle(self, *args, **options):
        from sensors.models import Sensor, SensorData

        # default yesterday
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        start_date = str2date(options.get('start_date'), yesterday)
        end_date = str2date(options.get('end_date'), yesterday)
        if options.get('type'):
            sensor_type = options.get('type').lower()
        else:
            sensor_type = "ppd42ns"

        if start_date > end_date:
            print("end_date is before start_date")
            return

        folder = "/opt/code/archive"

        for dt, sensor in product(self._dates(start_date, end_date), Sensor.objects.all()):
            # first only for ppd42ns.
            # because we need a list of fields for all other sensors
            # -> SENSOR_TYPE_CHOICES needs to become more sophisticated
            if not sensor.sensor_type.name.lower() == sensor_type:
                continue

            # location 11 is the dummy location. remove the datasets.
            # remove all indoor locations
            qs = SensorData.objects \
                .filter(sensor=sensor) \
                .filter(timestamp__date=dt) \
                .order_by("timestamp")
            if options.get('no_excludes'):
                qs = qs.exclude(location_id=11) \
                       .exclude(location__indoor=True)
            if not qs.exists():
                continue

            fn = '{date}_{stype}_sensor_{sid}.csv'.format(
                date=str(dt),
                stype=sensor.sensor_type.name.lower(),
                sid=sensor.id,
            )
            print(fn)
            os.makedirs(os.path.join(folder, str(dt)), exist_ok=True)

            # if file exists; overwrite. always
            key_list = []
            if sensor_type == 'ppd42ns':
                key_list = ['P1', 'durP1', 'ratioP1', 'P2', 'durP2', 'ratioP2']
            elif sensor_type in ['sht11', 'dht11', 'dht22', 'sht10', 'sht15']:
                key_list = ['temperature', 'humidity']
            elif sensor_type == "bmp180":
                key_list = ['pressure', 'altitude', 'pressure_sealevel', 'temperature']
            elif sensor_type == "photoresistor":
                key_list = ['brightness']

            with open(os.path.join(folder, str(dt), fn), "w") as fp:
                fp.write("sensor_id;sensor_type;location;lat;lon;timestamp;")
                fp.write(';'.join(key_list))
                fp.write("\n")
                for sd in qs:
                    sensordata = {
                        data['value_type']: data['value']
                        for data in sd.sensordatavalues.values('value_type', 'value')
                    }
                    if not sensordata:
                        continue
                    if sensor_type == 'ppd42ns' and 'P1' not in sensordata:
                        continue

                    longitude = ''
                    if sd.location.longitude:
                        longitude = "{:.3f}".format(sd.location.longitude)
                    latitude = ''
                    if sd.location.latitude:
                        latitude = "{:.3f}".format(sd.location.latitude)
                    s = ';'.join([str(sensor.id),
                                  sensor.sensor_type.name,
                                  str(sd.location.id),
                                  latitude,
                                  longitude,
                                  sd.timestamp.isoformat()])

                    fp.write(s)
                    fp.write(';')
                    fp.write(';'.join([sensordata.get(i, '') for i in key_list]))
                    fp.write("\n")

    @staticmethod
    def _dates(start, end):
        current = start
        while current <= end:
            yield current
            current += datetime.timedelta(days=1)
