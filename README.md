# feinstaub-api

Api to save data from sensors (especially particulates sensors).


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
docker-compose run web python3 manage.py reset_db
docker-compose run web python3 manage.py migrate
```

## production tutorial

for server installation protocol see:

https://github.com/opendata-stuttgart/meta/wiki/Protokoll-installation-von-feinstaub-api-server

### starting/creating docker instances

```
# database
docker run -d --name db-data -v /var/lib/postgres busybox
docker run -d --restart=always --volumes-from db-data --name feinstaub-db postgres:9.4

# home
docker run -d --name feinstaub-data -v /home/uid1000 aexea/aexea-base

# main image
docker build --tag=feinstaub-prod .
# reset database on first run
# docker run --rm -ti --volumes-from feinstaub-data --link feinstaub-db:db feinstaub-prod python3 manage.py reset_db
# docker run --rm -ti --volumes-from feinstaub-data --link feinstaub-db:db feinstaub-prod python3 manage.py createsuperuser
docker run -d --volumes-from feinstaub-data --link feinstaub-db:db --restart=always --name feinstaub feinstaub-prod
docker run --name feinstaub-nginx --net="host" --volumes-from feinstaub-data --restart=always -v `pwd`/nginx.conf:/etc/nginx/nginx.conf -d nginx


### rebuild, update

./update.sh
