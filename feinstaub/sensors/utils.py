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
    data = {
        'location': {
            'location': location.location,
            'indoor': location.indoor,
            'owner': location.owner.username,
            'description': location.description,
        },
    }
    table = sensordata_to_dataframe(location)
    data['table_head'] = table.columns
    data['table'] = table.values
    cache.set("location_cache_{}".format(location.pk),
              data,
              timeout=None)


def sensordata_to_dataframe(location):
    data_list = []
    for sensordata in SensorData.objects.filter(location=location):
        for datavalue in SensorDataValue.objects.filter(sensordata=sensordata):
            new_row = {
                'timestamp': [str(sensordata.timestamp)],
                'sensor': [sensordata.id],
                'value_type': [datavalue.value_type],
                'value': [datavalue.value],
                'sensor__owner': [sensordata.sensor.owner.username],
                'sampling_rate': [sensordata.sampling_rate],
            }
            data_list.append(new_row)
    df = pd.DataFrame(data_list,
                      columns=['timestamp', 'sensor', 'value_type',
                               'value', 'sensor__owner', 'sampling_rate'])
    return df


def export_to_csv():
    import csv
    with open('/tmp/data.csv', 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'type', 'indoor',
                      'location_id', 'sampling_rate']
        fieldnames += [i for i, j in SENSOR_TYPE_CHOICES]
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for element in SensorData.objects\
                                 .filter(sensor__sensor_type__name__in=[
                                     'dsm501a',
                                     'GP2Y1010AU0F',
                                     'PPD42NS'
                                 ]):
            d = {}
            d['timestamp'] = str(element.timestamp)
            d['type'] = element.sensor.sensor_type.name
            d['indoor'] = element.location.indoor
            d['location_id'] = element.location.pk
            d['sampling_rate'] = element.sampling_rate
            for data in element.sensordatavalues.all():
                d[data.value_type] = data.value
            csvwriter.writerow(d)