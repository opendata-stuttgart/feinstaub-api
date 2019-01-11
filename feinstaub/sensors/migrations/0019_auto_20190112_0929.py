# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-12 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0018_auto_20170218_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='description_internal',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='last_notify',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='sensor_position',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='city',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='country',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='industry_in_area',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='oven_in_area',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='postalcode',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='street_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='street_number',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='traffic_in_area',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sensordatavalue',
            name='value_type',
            field=models.CharField(choices=[('P0', '1µm particles'), ('P1', '1µm particles'), ('P2', '2.5µm particles'), ('durP1', 'duration 1µm'), ('durP2', 'duration 2.5µm'), ('ratioP1', 'ratio 1µm in percent'), ('ratioP2', 'ratio 2.5µm in percent'), ('samples', 'samples'), ('min_micro', 'min_micro'), ('max_micro', 'max_micro'), ('temperature', 'Temperature'), ('humidity', 'Humidity'), ('pressure', 'Pa'), ('altitude', 'meter'), ('pressure_sealevel', 'Pa (sealevel)'), ('brightness', 'Brightness'), ('dust_density', 'Dust density in mg/m3'), ('vo_raw', 'Dust voltage raw'), ('voltage', 'Dust voltage calculated'), ('P10', '1µm particles'), ('P25', '2.5µm particles'), ('durP10', 'duration 1µm'), ('durP25', 'duration 2.5µm'), ('ratioP10', 'ratio 1µm in percent'), ('ratioP25', 'ratio 2.5µm in percent'), ('door_state', 'door state (open/closed)'), ('lat', 'latitude'), ('lon', 'longitude'), ('height', 'height'), ('hdop', 'horizontal dilusion of precision'), ('timestamp', 'measured timestamp'), ('age', 'measured age'), ('satelites', 'number of satelites'), ('speed', 'current speed over ground'), ('azimuth', 'track angle')], db_index=True, max_length=100),
        ),
    ]
