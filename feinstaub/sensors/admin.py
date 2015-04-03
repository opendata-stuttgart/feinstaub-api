# coding=utf-8
from django.contrib import admin
from .models import (
    Sensor,
    SensorData,
    SensorDataValue,
    SensorLocation,
    SensorType, 
)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorDataValue)
class SensorDataValueAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorLocation)
class SensorLocationAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    pass
