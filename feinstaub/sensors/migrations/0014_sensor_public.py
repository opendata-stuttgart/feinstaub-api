# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0013_auto_20151025_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
