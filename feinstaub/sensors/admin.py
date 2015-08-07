# coding=utf-8
from django.contrib import admin
from .models import (
    Node,
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType,
)


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    search_fields = ['uid', 'description']
    list_display = ['uid', 'owner', 'location',
                    'description', 'created', 'modified']
    list_filter = ['owner', 'location']


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    search_fields = ['node__uid', 'description']
    list_display = ['node', 'pin', 'sensor_type',
                    'description', 'created', 'modified']
    list_filter = ['node__owner', 'sensor_type']


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    search_fields = ['sensor__uid', ]
    list_display = ['sensor', 'sampling_rate', 'timestamp',
                    'location', 'created', 'modified']
    list_filter = ['sensor', 'location', 'sensor__sensor_type']


@admin.register(SensorDataValue)
class SensorDataValueAdmin(admin.ModelAdmin):
    list_display = ['sensordata', 'value_type', 'value',
                    'created', 'modified']
    list_filter = ['value_type', 'sensordata__sensor',
                   'sensordata__sensor__sensor_type']
    readonly_fields = ['sensordata']


@admin.register(SensorLocation)
class SensorLocationAdmin(admin.ModelAdmin):
    search_fields = ['location', ]
    list_display = ['location', 'indoor', 'owner', 'description',
                    'timestamp', 'created', 'modified']
    list_filter = ['indoor', 'owner']


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    search_fields = ['uid', 'name', 'manufacturer', 'description']
    list_display = ['uid', 'name', 'manufacturer',
                    'description', 'created', 'modified']
