# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0006_auto_20150404_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordatavalue',
            name='sensordata',
            field=models.ForeignKey(to='sensors.SensorData', related_name='sensordatavalues'),
        ),
    ]
