from django import forms

from .models import SensorType


class AddSensordeviceForm(forms.Form):
    # more fields, see https://docs.djangoproject.com/en/1.10/ref/forms/fields/

    # get user information
    name_pate = forms.CharField(label='Your name', initial="")
    email_pate = forms.EmailField(label='Your email', required=True)
    # dbuser = forms.CharField(label='DB user', required=True) # get from login data

    # Location information
    # use exiting location possible?
    # maybe with selection from class SensorLocation(TimeStampedModel): location
    # and
    # use_location_fk = forms.BooleanField(label='use existing location', required=True, initial=False)
    # location: manual input
    location_location = forms.CharField(label='Location name (Address)', initial="")
    location_description = forms.CharField(label='Location description', initial="", widget=forms.Textarea)
    location_latitude = forms.DecimalField(label='Latitude (Breite, ~48)', min_value=-90, max_value=90, decimal_places=10)
    location_longitude = forms.DecimalField(label='Longitude (Länge, 9)', min_value=-180, max_value=180, decimal_places=10)

    # device info
    device_initials = forms.CharField(label='Device initials (label to write on device)')
    device_uid = forms.CharField(label='Device UID (esp8266-<chipid>)', initial="esp8266-")

    # Sensor info
    # multiple devices possible, have 2 as default
    # insert into model class Sensor(TimeStampedModel):

    # TODO: queryset
    #   class SensorType(TimeStampedModel): default: SDS011 14
    sensor1_type = forms.ModelChoiceField(queryset=SensorType.objects.all(), to_field_name="name", initial="SDS011")
    sensor1_pin = forms.DecimalField(label='PIN', min_value=0, max_value=8, decimal_places=0, initial=1)
    sensor1_description = forms.CharField(label='description for sensor 1', widget=forms.Textarea)
    sensor1_public = forms.BooleanField(label='public', required=True, initial=True)

    # TODO: queryset
    #   class SensorType(TimeStampedModel): default: DHT22 9
    sensor2_type = forms.ModelChoiceField(queryset=SensorType.objects.all(), to_field_name="name", initial="DHT22", empty_label='--- No sensor ---', required=False)
    sensor2_pin = forms.DecimalField(label='PIN', min_value=0, max_value=8, decimal_places=0, initial=7)
    # sensor description should contain deviceinitials+"_"+sensor1_type
    sensor2_description = forms.CharField(label='description for sensor 2')
    sensor2_public = forms.BooleanField(label='public', required=True, initial=True)
