# feinstaub-api

Api fuer das Abspeichern der Daten aus Feinstaubsensor.


## Installationsanleitung:

### virtualenv einrichen

(mit virtualenvwrapper)

``mkvirtualenv feinstaub-api -p /usr/bin/python3``

### Pakete installieren

```pip install -r requirements.txt```


## Mit Docker und Docker-Compose ausführen (development umgebung)

### Setup

* Installiere docker und Docker-Compose
* `docker-compose up -d`
* warten
* falls noch keine Datenbank existiert:
```
docker-compose run web python3 manage.py reset_db
docker-compose run web python3 manage.py migrate
```


