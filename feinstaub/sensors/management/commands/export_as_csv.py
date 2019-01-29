# coding=utf-8
import os
import datetime
from itertools import product
import boto3

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
        parser.add_argument('--upload_s3')

    def handle(self, *args, **options):
        from sensors.models import Sensor, SensorData

        # default yesterday
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        start_date = str2date(options.get('start_date'), yesterday)
        end_date = str2date(options.get('end_date'), yesterday)
        sensor_type = (options.get('type') or 'ppd42ns').lower()

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
            self._write_file(
                filepath=os.path.join(folder, str(dt), fn),
                qs=qs,
                sensor=sensor,
            )
            
            # Upload to s3
            if options.get('upload_s3'):
                # if file exists on s3; overwrite. always
                self._upload_csv(
                    tmp_path=os.path.join(folder, str(dt), fn),
                    dest_filename=os.path.join(str(dt), fn),
                    content_type="csv"
                )

    @staticmethod
    def _write_file(filepath, qs, sensor):
        sensor_type = sensor.sensor_type.name.lower()
        if sensor_type == 'ppd42ns' or sensor_type == 'sds011':
            key_list = ['P1', 'durP1', 'ratioP1', 'P2', 'durP2', 'ratioP2']
        elif sensor_type == 'pms1003' or sensor_type == 'pms3003' or sensor_type == 'pms5003' or sensor_type == 'pms6003' or sensor_type == 'pms7003':
            key_list = ['P1', 'P2', 'P0']
        elif sensor_type in ['ds18b20']:
            key_list = ['temperature']
        elif sensor_type in ['dht11', 'dht22', 'htu21d', 'sht10', 'sht11', 'sht15']:
            key_list = ['temperature', 'humidity']
        elif sensor_type == "bmp180" or sensor_type == 'bpm280':
            key_list = ['pressure', 'altitude', 'pressure_sealevel', 'temperature']
        elif sensor_type == "bme280":
            key_list = ['pressure', 'altitude', 'pressure_sealevel', 'temperature','humidity']
        elif sensor_type == "photoresistor":
            key_list = ['brightness']
        else:
            key_list = []

        with open(filepath, "w") as fp:
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

    @staticmethod
    def _upload_csv(tmp_path, dest_filename, content_type):
        bucket_name = os.getenv('AWS_BUCKET_NAME')
        access_key = os.getenv('AWS_ACCESS_KEY')
        secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        url_prefix = os.getenv('AWS_URL_PREFIX')
        region = os.getenv('AWS_REGION')

        dest_path = os.path.join(url_prefix, dest_filename)
        url = 'http://s3-%s.amazonaws.com/%s/%s' % (region, bucket_name, dest_path)

        session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_access_key,
                                region_name=region)
        s3 = session.resource('s3')

        bucket = s3.Bucket(bucket_name)
        try:
            bucket.upload_file(tmp_path, dest_path, ExtraArgs={'ContentType': content_type,
                                                               'ContentDisposition': 'attachment',
                                                               'ACL': "public-read"})
            return url
        except IOError as e:
            return None
