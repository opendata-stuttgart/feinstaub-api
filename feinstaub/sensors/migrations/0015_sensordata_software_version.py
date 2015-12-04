# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0014_sensor_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='software_version',
            field=models.CharField(help_text='sensor software version', default='', max_length=100),
        ),
    ]
