# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0011_auto_20150807_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='node',
            field=models.ForeignKey(default=1, to='sensors.Node'),
            preserve_default=False,
        ),
    ]
