# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sensors', '0003_auto_20150330_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorDataValue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(editable=False, default=django.utils.timezone.now, blank=True, verbose_name='modified')),
                ('value', models.TextField()),
                ('value_type', models.CharField(choices=[('P1', '1µm particles'), ('P2', '2.5µm particles'), ('temperature', 'Temperature'), ('humidity', 'Humidity'), ('brightness', 'Brightness')], max_length=100)),
                ('sensordata', models.ForeignKey(to='sensors.SensorData')),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='sensordata',
            name='value1',
        ),
        migrations.RemoveField(
            model_name='sensordata',
            name='value2',
        ),
        migrations.RemoveField(
            model_name='sensorlocation',
            name='sensor',
        ),
        migrations.AddField(
            model_name='sensor',
            name='location',
            field=models.ForeignKey(default=False, to='sensors.SensorLocation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensordata',
            name='location',
            field=models.ForeignKey(default=1, blank=True, to='sensors.SensorLocation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='indoor',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sensorlocation',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='If not set, location is public.', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
