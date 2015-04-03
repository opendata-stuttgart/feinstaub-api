# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0004_auto_20150331_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorlocation',
            name='indoor',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensortype',
            name='description',
            field=models.CharField(max_length=10000, blank=True, null=True),
            preserve_default=True,
        ),
    ]
