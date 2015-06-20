# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0009_auto_20150503_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordatavalue',
            name='value',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='sensordatavalue',
            name='value_type',
            field=models.CharField(choices=[('P1', '1µm particles'), ('P2', '2.5µm particles'), ('durP1', 'duration 1µm'), ('durP2', 'duration 2.5µm'), ('ratioP1', 'ratio 1µm in percent'), ('ratioP2', 'ratio 2.5µm in percent'), ('temperature', 'Temperature'), ('humidity', 'Humidity'), ('pressure', 'Pa'), ('altitude', 'meter'), ('pressure_sealevel', 'Pa (sealevel)'), ('brightness', 'Brightness'), ('dust_density', 'Dust density in mg/m3'), ('vo_raw', 'Dust voltage raw'), ('voltage', 'Dust voltage calculated'), ('P10', '1µm particles'), ('P25', '2.5µm particles'), ('durP10', 'duration 1µm'), ('durP25', 'duration 2.5µm'), ('ratioP10', 'ratio 1µm in percent'), ('ratioP25', 'ratio 2.5µm in percent')], max_length=100, db_index=True),
        ),
    ]
