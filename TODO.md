# Form to add sensors

## Paten table

* create a contact table for "Paten"? NO, to description
    * at least email, pseudonym, name, optional: road, houseno, PLZ, City, country
    * optional: might be linked to (one, n-1) sensorlocation?

currently description fields are misused for this

## Form input processing

as in feinstaub/sensors/forms.py

TODO:
* access only for AUTH users
* save form
* take DB user from AUTH
* step 1:
	* create new location from location_*
* step 2:
	* create node description from user data + description,
        * device_uid
        * description = description + device_initials (name to be written on chip, might be derived from user data, optional: with counter)
	* insert node, get nodeID
* step 2:
    * multiple sensors to be inserted, insert two
    * two sensors,
        * select sensor_type, senpin
        * check for second sensor_type == '--- No sensor ---'
        * select type of sensor, pin
        * add to description: device_initials and sensor_type, e.g. "AA2-DHT"

# code examples

from https://gist.github.com/mfa/cb97982a4b3874ab2e8f5453d5077782
