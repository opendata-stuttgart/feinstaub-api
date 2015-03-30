# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensordata',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 18, 0, 43, 397896, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 30, 18, 0, 43, 398539, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
