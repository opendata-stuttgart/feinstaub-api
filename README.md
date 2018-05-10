# sensors.AFRICA Air Quality API [![Build Status](https://travis-ci.org/CodeForAfricaLabs/sensors.AFRICA-AQ-api.svg?branch=master)](https://travis-ci.org/CodeForAfricaLabs/sensors.AFRICA-AQ-api)

Api to save data from sensors (especially particulates sensors).

## Note

Daily CSV dumps: http://archive.luftdaten.info/

## Installation:

### virtualenv

(with virtualenvwrapper)

``mkvirtualenv feinstaub-api -p /usr/bin/python3``

### install packets

```pip install -r requirements.txt```


## using docker and docker-compose (for development)

### Setup

* install docker and docker-compose
* `docker-compose up -d`
* wait
* maybe create a database (if non existent):
```
docker-compose run --rm web python3 manage.py reset_db
docker-compose run --rm web python3 manage.py migrate
```

## production tutorial

for server installation protocol see:

https://github.com/opendata-stuttgart/meta/wiki/Protokoll-installation-von-feinstaub-api-server

### setup of production.py

* copy ``feinstaub/settings/production_example.py`` to ``feinstaub/settings/production.py``
* CHANGE the annotated things. really!


### starting/creating docker instances

```
# database
docker run -d --restart=always -v $(pwd)/../feinstaub-db-data:/var/lib/postgres --name feinstaub-db postgres:9.6

# redis
docker run -d --restart=always -v $(pwd)/../feinstaub-redis-data:/data --name feinstaub-redis redis redis-server

# home
docker run -d --name feinstaub-data -v /home/uid1000 aexea/aexea-base

# main image
docker build --tag=feinstaub-prod .
# reset database on first run
# docker run --rm -ti -v $(pwd)/../feinstaub-data:/home/uid1000 --link feinstaub-db:db feinstaub-prod python3 manage.py reset_db
# docker run --rm -ti -v $(pwd)/../feinstaub-data:/home/uid1000 --link feinstaub-db:db feinstaub-prod python3 manage.py migrate
# docker run --rm -ti -v $(pwd)/../feinstaub-data:/home/uid1000 --link feinstaub-db:db feinstaub-prod python3 manage.py createsuperuser
docker run -d -v $(pwd)/../feinstaub-data:/home/uid1000 --link feinstaub-db:db --link feinstaub-redis:redis --restart=always --name feinstaub feinstaub-prod
docker run --name feinstaub-nginx --net="host" -v $(pwd)/../feinstaub-data:/home/uid1000 --restart=always -v `pwd`/nginx.conf:/etc/nginx/nginx.conf -d nginx:1.11


### rebuild, update

./update.sh
```


### Notes

## swap

512mb on server are not enough.
create swap using:
```
sudo dd if=/dev/zero of=/swapfile bs=1024 count=524288
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

To make the swap reboot persistent add the following line in `/etc/fstab`:
```
/swapfile   swap    swap    defaults        0       0
```

## production database for development

### on production

``
docker exec feinstaub-db pg_dump -Fc -h localhost -v -U postgres feinstaub > feinstaub-backup.sql
``

even better:  
``
docker run --rm -ti -v `pwd`:/root --link feinstaub-db:db postgres:9.4 pg_dump -U postgres -h db feinstaub -f /root/feinstaub-db.pgdump
``

### on development

get ipaddress of postgres-container:
``
docker inspect feinstaubapi_db_1 | grep IPAddress
``

restore database:
``
pg_restore -C -v -h [ipaddress-of-db-container] -U postgres -d feinstaub feinstaub-backup.sql
``

#### dump development database

add volume mount to db container:
```
  volumes:
   - .:/opt/code
```

and run dump command:

```
docker-compose run --rm db pg_dump -Fc -h db -v -U postgres feinstaub -f /opt/code/feinstaub-api-db.dump
```

---

## Deployement

To deploy the API, we use Dokku.

```
 # for debian systems, installs dokku via apt-get
 $ wget https://raw.githubusercontent.com/dokku/dokku/v0.11.3/bootstrap.sh
 $ sudo DOKKU_TAG=v0.11.3 bash bootstrap.sh
 # go to your server's IP and follow the web installer
```

### Install + Create Dependencies

Once installed, we can do the following:

1. Create the Dokku app and add a domain to it

```
dokku apps:create sensors-aq-api
```
2. Install Postgres (Optional)

This is an optional step if you'd like to have Postgres installed locally;

```
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git postgres
dokku postgres:create sensors-aq-api-postgres

```

### Config

```
dokku config:set sensors-aq-api \
    API_SECRET_KEY=... \
    API_FORECAST_IO_KEY=... \
    HOST_DIR=$(pwd)/../feinstaub-data\
    POSTGRESQL_DATABASE=... \
    POSTGRESQL_USERNAME=... \
    POSTGRESQL_HOST=... \
    POSTGRESQL_PORT... \
    AWS_BUCKET_NAME=... \
    AWS_URL_PREFIX=... \
    AWS_SECRET_ACCESS_KEY=... \
    AWS_REGION=... \
    AWS_ACCESS_KEY=... \

dokku proxy:ports-add sensors-aq-api http:80:8000

```

# Deploy
```
git remote add dokku dokku@api.aq.sensors.africa:sensors-aq-api
git push dokku
```

---

# License

Copyright (c) 2018 Code for Africa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
