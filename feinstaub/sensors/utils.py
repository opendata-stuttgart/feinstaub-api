from .models import (
    SensorData,
    SensorDataValue,
    SENSOR_TYPE_CHOICES,
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
