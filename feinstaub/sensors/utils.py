from django.core.cache import cache
import pandas as pd

from .models import (
    SensorData,
    SensorDataValue,
    SensorLocation,
    SENSOR_TYPE_CHOICES,
)


def calculate_datatable():
    for location in SensorLocation.objects.all():
        calculate_datatable_location(location)


def calculate_datatable_location(location):
    # calculate for each location per day a table with all sensor values
    table = sensordata_to_dataframe(location)

    data = {
        'location': {
            'location': location.location,
            'indoor': location.indoor,
            'owner': location.owner.username,
            'description': location.description,
        },
        'table_head': table.columns,
        'table': table.values,
    }

    cache.set(
        'location_cache_{}'.format(location.pk),
        data,
        timeout=None,
    )


def sensordata_to_dataframe(location):
    data_list = [
        {
            'timestamp': [str(sensordata.timestamp)],
            'sensor': [sensordata.id],
            'value_type': [datavalue.value_type],
            'value': [datavalue.value],
            'sensor__owner': [sensordata.sensor.owner.username],
            'sampling_rate': [sensordata.sampling_rate],
        }
        for sensordata in SensorData.objects.filter(location=location)
        for datavalue in sensordata.sensordatavalues.all()
    ]

    return pd.DataFrame(
        data_list,
        columns=['timestamp', 'sensor', 'value_type', 'value', 'sensor__owner',
                 'sampling_rate'],
    )


def export_to_csv():
    import csv

    fieldnames = ['timestamp', 'type', 'indoor',
                  'location_id', 'sampling_rate']
    fieldnames += [i for i, j in SENSOR_TYPE_CHOICES]

    with open('/tmp/data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        elements = SensorData.objects \
            .filter(sensor__sensor_type__name__in=[
                'dsm501a',
                'GP2Y1010AU0F',
                'PPD42NS',
            ]) \
            .values(
                'pk', 'timestamp', 'sensor__sensor_type__name',
                'location__indoor', 'location__pk', 'sampling_rate',
            )

        for element in elements:
            d = {
                'timestamp': str(element['timestamp']),
                'type': element['sensor__sensor_type__name'],
                'indoor': element['location__indoor'],
                'location_id': element['location__pk'],
                'sampling_rate': element['sampling_rate'],
            }

            d.update(dict(
                SensorDataValue.objects
                .filter(sensordata_id=element['pk'])
                .values_list('value_type', 'value')
            ))

            csvwriter.writerow(d)
