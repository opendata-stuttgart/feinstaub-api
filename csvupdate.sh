#!/bin/bash

docker-compose run web reset_db --noinput
zcat /home/feinstaub/dbbackup/`date +%Y-%m-%d`.pgdump.gz | docker-compose run db psql -h db -U postgres feinstaub
docker-compose run web export_as_csv
docker-compose stop
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
