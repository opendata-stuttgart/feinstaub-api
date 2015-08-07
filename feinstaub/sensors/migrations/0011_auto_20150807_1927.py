# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_extensions.db.fields
import django.utils.timezone


def migrate_sensor(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Sensor = apps.get_model("sensors", "Sensor")
    Node = apps.get_model("sensors", "Node")
    for sensor in Sensor.objects.all():
        print("sensor: {}".format(sensor.id))
        node = Node.objects.create(uid=sensor.uid,
                                   description=sensor.description,
                                   owner=sensor.owner,
                                   location=sensor.location)
        sensor.node = node
        sensor.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sensors', '0010_auto_20150620_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('uid', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['uid'],
            },
        ),
        migrations.AddField(
            model_name='node',
            name='location',
            field=models.ForeignKey(to='sensors.SensorLocation'),
        ),
        migrations.AddField(
            model_name='node',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sensor',
            name='node',
            field=models.ForeignKey(to='sensors.Node', blank=True, null=True),
            preserve_default=False,
        ),

        migrations.RunPython(
            migrate_sensor,
        ),

        migrations.AlterModelOptions(
            name='sensor',
            options={},
        ),
        migrations.AlterModelOptions(
            name='sensorlocation',
            options={'ordering': ['location']},
        ),
        migrations.AlterModelOptions(
            name='sensortype',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='sensor',
            name='pin',
            field=models.CharField(max_length=10, help_text='differentiate the sensors on one node by giving pin used', default='-'),
        ),
        migrations.AlterField(
            model_name='sensordatavalue',
            name='value_type',
            field=models.CharField(db_index=True, max_length=100, choices=[('P1', '1µm particles'), ('P2', '2.5µm particles'), ('durP1', 'duration 1µm'), ('durP2', 'duration 2.5µm'), ('ratioP1', 'ratio 1µm in percent'), ('ratioP2', 'ratio 2.5µm in percent'), ('temperature', 'Temperature'), ('humidity', 'Humidity'), ('pressure', 'Pa'), ('altitude', 'meter'), ('pressure_sealevel', 'Pa (sealevel)'), ('brightness', 'Brightness'), ('dust_density', 'Dust density in mg/m3'), ('vo_raw', 'Dust voltage raw'), ('voltage', 'Dust voltage calculated'), ('P10', '1µm particles'), ('P25', '2.5µm particles'), ('durP10', 'duration 1µm'), ('durP25', 'duration 2.5µm'), ('ratioP10', 'ratio 1µm in percent'), ('ratioP25', 'ratio 2.5µm in percent'), ('door_state', 'door state (open/closed)')]),
        ),
        migrations.AlterUniqueTogether(
            name='sensor',
            unique_together=set([('node', 'pin')]),
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='location',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='uid',
        ),
    ]
