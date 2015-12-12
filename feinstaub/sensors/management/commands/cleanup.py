# coding=utf-8
from django.core.management import BaseCommand
import datetime


class Command(BaseCommand):

    help = "Cleanup sensordata. This management command may change over time."

    def handle(self, *args, **options):
        from sensor.models import SensorData
        from django.db.models import Count

        # delete all SensorData without any SensorDataValues, older than today (maybe some are written just now).
        SensorData.objects.annotate(Count('sensordatavalues')).filter(sensordatavalues__count=0).filter(created__lt=datetime.date.today()).delete()

        # find all ppd42ns with wrong values and delete them. fixing is way to complicated
        SensorData.objects.filter(sensor_id__in=[34, 39, 60]).filter(sensordatavalues__value_type="temperature").delete()
        SensorData.objects.filter(sensor_id__in=[34, 39, 60]).filter(sensordatavalues__value_type="humidity").delete()
