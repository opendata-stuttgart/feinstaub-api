# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uid', models.SlugField(unique=True)),
                ('description', models.CharField(max_length=10000)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ('-modified', '-created'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('value1', models.IntegerField()),
                ('value2', models.IntegerField(blank=True, null=True)),
                ('sensor', models.ForeignKey(to='sensors.Sensor')),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ('-modified', '-created'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('location', models.TextField(blank=True, null=True)),
                ('sensor', models.ForeignKey(to='sensors.Sensor')),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ('-modified', '-created'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uid', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('manufacturer', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=10000)),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ('-modified', '-created'),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(to='sensors.SensorType'),
            preserve_default=True,
        ),
    ]
