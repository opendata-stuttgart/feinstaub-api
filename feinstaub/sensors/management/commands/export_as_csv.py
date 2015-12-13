# coding=utf-8
import os
from django.core.management import BaseCommand
import datetime


def str2date(str):
    return datetime.datetime.strptime(str, '%Y-%m-%d').date()


class Command(BaseCommand):

    help = "Dump all Sensordata to csv files"

    def add_arguments(self, parser):
        parser.add_argument('--start_date')
        parser.add_argument('--end_date')

    def handle(self, *args, **options):
        from sensors.models import Sensor, SensorData

        # default yesterday
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        start_date = options.get('start_date')
        if not start_date:
            start_date = str(yesterday)
        end_date = options.get('end_date')
        if not end_date:
            end_date = str(yesterday)

        if start_date > end_date:
            print("end_date is before start_date")
            return

        dt = str2date(start_date)

        while dt <= str2date(end_date):

            folder = "/opt/code/archive"
            for sensor in Sensor.objects.all():
                # first only for ppd42ns.
                # because we need a list of fields for all other sensors -> SENSOR_TYPE_CHOICES needs to become more sophisticated
                if not sensor.sensor_type.name.lower() == "ppd42ns":
                    continue

                fn = "{date}_{stype}_sensor_{sid}.csv".format(sid=sensor.id, stype=sensor.sensor_type.name.lower(), date=str(dt))
                # if file exists; overwrite. always
                print(fn)
                with open(os.path.join(folder, fn), "w") as fp:
                    fp.write("sensor_id;sensor_type;location;timestamp;")
                    # FIXME: generate from SENSOR_TYPE_CHOICES
                    fp.write("P1;durP1;ratioP1;P2;durP2;ratioP2\n")
                    for sd in SensorData.objects.filter(sensor=sensor).filter(timestamp__date=dt).order_by("timestamp"):
                        s = ';'.join([str(sensor.id), sensor.sensor_type.name, str(sd.location.id), str(sd.timestamp.date())])
                        fp.write(s)
                        fp.write('{};'.format(sd.sensordatavalues.get(value_type="P1").value))
                        fp.write('{};'.format(sd.sensordatavalues.get(value_type="durP1").value))
                        fp.write('{};'.format(sd.sensordatavalues.get(value_type="ratioP1").value))
                        fp.write('{};'.format(sd.sensordatavalues.get(value_type="P2").value))
                        fp.write('{};'.format(sd.sensordatavalues.get(value_type="durP2").value))
                        fp.write('{}'.format(sd.sensordatavalues.get(value_type="ratioP2").value))
                        fp.write("\n")

            dt += datetime.timedelta(days=1)
