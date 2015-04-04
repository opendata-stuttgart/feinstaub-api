# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0005_auto_20150403_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensordatavalue',
            name='value_type',
            field=models.CharField(max_length=100, choices=[('P1', '1µm particles'), ('P2', '2.5µm particles'), ('durP1', 'duration 1µm'), ('durP2', 'duration 2.5µm'), ('ratioP1', 'ratio 1µm in percent'), ('ratioP2', 'ratio 2.5µm in percent'), ('temperature', 'Temperature'), ('humidity', 'Humidity'), ('brightness', 'Brightness')]),
        ),
    ]
