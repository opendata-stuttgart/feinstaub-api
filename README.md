# feinstaub-api

Api fuer das Abspeichern der Daten der Feinstaubsensoren.


## Installationsanleitung:

### virtualenv einrichen

(mit virtualenvwrapper)

``mkvirtualenv feinstaub-api -p /usr/bin/python3``

### Pakete installieren

```pip install -r requirements.txt```


## Mit Docker und Docker-Compose ausführen (Enwicklungsumgebung)

### Setup

* Installiere Docker und Docker-Compose
* `docker-compose up -d`
* warten
* falls noch keine Datenbank existiert:
```
docker-compose run web python3 manage.py reset_db
docker-compose run web python3 manage.py migrate
```

## Production-Deployment-Anleitung

https://github.com/opendata-stuttgart/meta/wiki/Protokoll-installation-von-feinstaub-api-server
